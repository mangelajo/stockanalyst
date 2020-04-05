
class ETFHolding(object):
    def __init__(self, name, sym, weight):
        self.name = name
        self.symbol = sym
        self.weight = weight

class ETFDBCSV(object):
    def __init__(self, path):
        self._details = {}
        self._components = []
        self._components_dict = {}
        self._read_file(path)

    @property
    def components(self):
        return self._components

    def getComponent(self, symbol):
        return self._components_dict[symbol]

    def _read_file(self, path):
        with open(path, 'r') as f:
            line = f.readline().strip('\n ')
            while ':' in line:
                parts = line.split(':')
                self._details[parts[0].strip(' ')] = parts[1].strip(' ')
                line = f.readline().strip(' \n')

            while line == "":
                line = f.readline().strip(' \n')

            assert(line=='Holding,Symbol,Weighting')

            for line in f:
                line = line.strip('\n ')
                parts = line.split(',')
                data = ETFHolding(parts[0],
                                  parts[1],
                                  float(parts[2].strip('%')) / 100.0)

                self._components_dict[data.symbol] = data
                self._components.append(data)

