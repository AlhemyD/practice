from gnss_tec import rnx

def parsing(file_name: str):
    with open(file_name) as obs_file:
        reader = rnx(obs_file)
        for tec in reader:
            print(
                '{} {}: {} {}'.format(
                    tec.timestamp,
                    tec.satellite,
                    tec.phase_tec,
                    tec.p_range_tec,
                )
            )
