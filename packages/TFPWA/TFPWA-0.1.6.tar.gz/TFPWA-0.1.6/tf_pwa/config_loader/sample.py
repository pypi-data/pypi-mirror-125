import copy

from tf_pwa.amp.core import get_particle_model_name
from tf_pwa.cal_angle import cal_angle_from_momentum
from tf_pwa.config import get_config
from tf_pwa.data import data_mask, data_merge, data_shape
from tf_pwa.particle import BaseParticle
from tf_pwa.phasespace import generate_phsp as generate_phsp_o
from tf_pwa.tensorflow_wrapper import tf

from .config_loader import ConfigLoader


@ConfigLoader.register_function()
def generate_toy(config, N=1000, force=True, max_N=100000):
    decay_group = config.get_decay()
    amp = config.get_amplitude()

    def gen(M):
        return generate_phsp(config, M)

    all_data = []
    n_gen = 0
    n_accept = 0
    n_total = 0
    test_N = 10 * N
    while N > n_accept:
        test_N = abs(min(max_N, test_N))
        data = single_sampling(gen, amp, test_N)
        n_gen = data_shape(data)
        n_total += test_N
        n_accept += n_gen
        test_N = int(1.01 * n_total / (n_accept + 1) * (N - n_accept))
        all_data.append(data)

    ret = data_merge(*all_data)

    if force:
        cut = tf.range(data_shape(ret)) < N
        ret = data_mask(ret, cut)

    return ret


def single_sampling(phsp, amp, N):
    data = phsp(N)
    weight = amp(data)
    rnd = tf.random.uniform(weight.shape, dtype=weight.dtype)
    cut = rnd * tf.reduce_max(weight) * 1.1 < weight
    data = data_mask(data, cut)
    return data


@ConfigLoader.register_function()
def generate_toy2(
    config,
    N=1000,
    force=True,
    gen=None,
    gen_p=None,
    max_N=100000,
    include_charge=False,
):
    """
    A more accurate method for generating toy data.

    :param N: number of events.
    :param force: if romove extra data generated.
    :param gen: optional function for generate phase space, the return value is same as config.get_data.
    :param gen_p:  optional function for generate phase space, the return value is dict as `{B: pb, C: pc, D: pd}`.
    :param max_N: max number of events for every try.

    """

    decay_group = config.get_decay()
    amp = config.get_amplitude()

    if gen is None:
        if gen_p is not None:

            def gen(N):
                p = gen_p(N)
                p = {
                    BaseParticle(k) if isinstance(k, str) else k: v
                    for k, v in p.items()
                }
                return cal_angle_from_momentum(p, config.get_decay(False))

        else:

            def gen(M):
                return generate_phsp(config, M)

    all_data = []
    n_gen = 0
    n_accept = 0
    n_total = 0
    test_N = 10 * N
    if not hasattr(config, "max_amplitude"):
        config.max_amplitude = None

    while N > n_accept:
        test_N = abs(min(max_N, test_N))
        data, new_max_weight = single_sampling2(
            gen,
            amp,
            test_N,
            config.max_amplitude,
            include_charge=include_charge,
        )
        n_gen = data_shape(data)
        n_total += test_N
        if (
            config.max_amplitude is not None
            and new_max_weight > config.max_amplitude
            and len(all_data) > 0
        ):
            tmp = data_merge(*all_data)
            rnd = tf.random.uniform(
                (n_accept,), dtype=config.max_amplitude.dtype
            )
            cut = rnd * new_max_weight / config.max_amplitude < 1.0
            tmp = data_mask(tmp, cut)
            all_data = [tmp]
            n_accept = data_shape(tmp)
        else:
            config.max_amplitude = new_max_weight
        n_accept += n_gen
        test_N = int(1.01 * n_total / (n_accept + 1) * (N - n_accept))
        all_data.append(data)

    ret = data_merge(*all_data)

    if force:
        cut = tf.range(data_shape(ret)) < N
        ret = data_mask(ret, cut)

    return ret


def single_sampling2(phsp, amp, N, max_weight=None, include_charge=False):
    data = phsp(N)
    if "charge_conjugation" not in data:
        if include_charge:
            charge = (
                tf.cast(
                    tf.random.uniform((data_shape(data),)) > 0.5,
                    get_config("dtype"),
                )
                * 2
                - 1
            )
            data["charge_conjugation"] = charge
        else:
            data["charge_conjugation"] = tf.ones(
                (data_shape(data),), get_config("dtype")
            )
    weight = amp(data)
    new_max_weight = tf.reduce_max(weight)
    if max_weight is None or max_weight < new_max_weight:
        max_weight = new_max_weight * 1.01
    rnd = tf.random.uniform(weight.shape, dtype=weight.dtype)
    cut = rnd * max_weight < weight
    data = data_mask(data, cut)
    return data, max_weight


@ConfigLoader.register_function()
def generate_phsp_p(config, N=1000):
    decay_group = config.get_decay()

    m0, mi, idx = build_phsp_chain(decay_group)

    pi = generate_phsp_o(m0, mi, N=N)

    def loop_index(tree, idx):
        for i in idx:
            tree = tree[i]
        return tree

    return {k: loop_index(pi, idx[k]) for k in decay_group.outs}


@ConfigLoader.register_function()
def generate_phsp(config, N=1000):
    p = generate_phsp_p(config, N)
    return cal_angle_from_momentum(p, config.get_decay(False))


def build_phsp_chain(decay_group):
    struct = decay_group.topology_structure()
    inner_node = [set(i.inner) for i in struct]
    a = inner_node[0]
    for i in inner_node[1:]:
        a = a & i

    m0 = decay_group.top.get_mass()
    mi = [i.get_mass() for i in decay_group.outs]

    if any(i is None for i in [m0] + mi):
        raise ValueError("mass required to generate phase space")

    m0 = float(m0)
    mi = [float(i) for i in mi]

    if len(a) == 0:
        return m0, mi, {k: (v,) for v, k in enumerate(decay_group.outs)}

    # print(type(decay_group.get_particle("D")))
    # print([type(i) for i in decay_group[0].inner])

    ref_dec = decay_group[0]

    decay_map = struct[0].topology_map(ref_dec)
    # print(decay_map)
    nodes = []
    for i in a:
        if get_particle_model_name(decay_map[i]) == "one":
            nodes.append((i, float(decay_map[i].get_mass())))

    mi = dict(zip(decay_group.outs, mi))

    st = struct[0].sorted_table()
    mi, final_idx = build_phsp_chain_sorted(st, mi, nodes)
    return m0, mi, final_idx


def build_phsp_chain_sorted(st, final_mi, nodes):
    """
    {A: [B,C, D], R: [B,C]} + {R: M} => ((mr, (mb, mc)), md)
    """
    st = copy.deepcopy(st)
    for i in final_mi:
        del st[i]
    mass_table = final_mi.copy()
    final_idx = {}
    index_root_map = {}
    # print(st)
    max_iter = 10
    while nodes and max_iter > 0:
        pi, mi = nodes.pop(0)
        sub_node = st[pi]
        max_iter -= 1
        if all(i in mass_table for i in sub_node):
            index_root_map[pi] = sub_node
            # the order make the following loop work
            mass_table[pi] = (mi, [mass_table[i] for i in sub_node])
            for k, i in enumerate(sub_node):
                final_idx[i] = (k,)
                del mass_table[i]
            for k, v in st.items():
                if k == pi:
                    continue
                if all(i in v for i in sub_node):
                    for n in sub_node:
                        st[k].remove(n)
                    st[k].append(pi)
        else:
            nodes.append((pi, mi))
    # print(mass_table)
    ret = []
    for k, i in enumerate(mass_table):
        if i in final_mi:
            final_idx[i] = (k,)
        else:
            for j in index_root_map[i]:
                final_idx[j] = (k, *final_idx[j])
        ret.append(mass_table[i])
    # assert False
    return ret, final_idx
