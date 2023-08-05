import os

class DdpEnvInitializer:
    # 01013-01014   -> [01013, 01014]
    @staticmethod
    def _flatten_ranged_hosts(prefix, host_range):
        res = []
        ranges = host_range.split('-')
        w = len(ranges[0])
        start = int(ranges[0])
        end = int(ranges[1])
        while start <= end:
            res.append(prefix + format(start, f'0{w}d'))
            start += 1

        return res

    # 'cnhtc-gpu-p[01005,01007,01013-01014]'  -> ['cnhtc-gpu-p01005', 'cnhtc-gpu-p01007', 'cnhtc-gpu-p01013', 'cnhtc-gpu-p01014']
    @staticmethod
    def _flatten_hosts(hosts):
        host_list = []
        idx = hosts.find('[')
        if idx == -1:
            host_list.append(hosts)
            return host_list

        prefix = hosts[0:idx]
        suffix = hosts[idx + 1:-1]

        suffix_list = suffix.split(',')
        for host_suffix in suffix_list:
            if '-' not in host_suffix:
                host_list.append(prefix + host_suffix)
            else:
                host_list.extend(DdpEnvInitializer._flatten_ranged_hosts(prefix, host_suffix))
        # print(host_list)
        return host_list

    @staticmethod
    def setup_env():
        nodes = int(os.environ.get('SLURM_JOB_NUM_NODES', 0))
        if nodes <= 1:
            return
        node_name = os.environ.get('SLURMD_NODENAME', '')
        node_list_str = os.environ.get('SLURM_JOB_NODELIST', '')
        if not node_name or not node_list_str:
            raise Exception('SLURMD_NODENAME or SLURM_JOB_NODELIST is not set in environment variables')
        node_list = DdpEnvInitializer._flatten_hosts(node_list_str)
        node_idx = node_list.index(node_name)
        os.environ['MASTER_PORT'] = '8888'
        os.environ['MASTER_ADDR'] = node_list[0]
        os.environ['WORLD_SIZE'] = str(len(node_list))
        os.environ['NODE_RANK'] = str(node_idx)
        for k, v in os.environ.items():
            print(f'{k}: [{v}]')

    @staticmethod
    def getGpus():
        return int(os.environ.get('SLURM_GPUS_PER_NODE', 8))

    @staticmethod
    def getNodes():
        return int(os.environ.get('SLURM_JOB_NUM_NODES', 1))