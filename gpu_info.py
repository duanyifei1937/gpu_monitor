#!/data/soft/python3.6/bin/python3.6
# -*- coding: utf-8 -*-

import os


def get_cmd_from_pid(pid):
    cmd_file = '/proc/%d/cmdline' % pid
    if not os.path.exists(cmd_file):
        raise ValueError('%s doesn\'t exists!' % cmd_file)
    cmd = os.popen('cat %s | xargs -0 echo' % cmd_file)
    info = cmd.read().strip()
    cmd.close()
    return info


def parse_gpu_usage_str(info=None):
    """ parse the output of `nvidia-smi` and get the gpu usage info
    :param info: output string of `nvidia-smi`
    :returns: a dict of gpu usage info.
    """
    if info is None:
        cmd = os.popen('nvidia-smi')
        info = cmd.read()
        cmd.close()

    if info == '':
        return {}

    gpus = {}
    is_gpu_list = True
    gpu_id = None
    lines = info.split('\n')
    k = 7
    while k < len(lines):
        l = lines[k]
        t = l.split()

        if len(t) == 0:
            is_gpu_list = False

        if is_gpu_list:
            try:
                _id = int(t[1])
                gpu_id = _id
                t2 = lines[k+1].split()
                used_gm = int(t2[-7][:-3])
                gm = int(t2[-5][:-3])
                usage = int(t2[-3][:-1])
                gpus[gpu_id] = {
                    'used_memory': used_gm,
                    'memory': gm,
                    'usage': usage,
                    'process': [],
                }
            except:
                pass
        else:
            try:
                _id = int(t[1])
                pid = int(t[2])
                cmd = get_cmd_from_pid(pid)
                used_gm = int(t[5][:-3])
                gpus[_id]['process'].append((pid, cmd, used_gm))
            except:
                pass

        k += 1

    return gpus


if __name__ == '__main__':
    print(parse_gpu_usage_str())
