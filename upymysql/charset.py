MBLENGTH = {
        8:1,
        33:3,
        88:2,
        91:2
        }


class Charset(object):
    def __init__(self, id, name, collation, is_default):
        self.id, self.name, self.collation = id, name, collation
        self.is_default = is_default == 'Yes'

    def __repr__(self):
        return "Charset(id=%s, name=%r, collation=%r)" % (
                self.id, self.name, self.collation)

    @property
    def encoding(self):
        name = self.name
        if name == 'utf8mb4':
            return 'utf8'
        return name

    @property
    def is_binary(self):
        return self.id == 63


class Charsets:
    def __init__(self):
        self._by_id = {}

    def add(self, c):
        self._by_id[c.id] = c

    def by_id(self, id):
        return self._by_id[id]

    def by_name(self, name):
        name = name.lower()
        for c in self._by_id.values():
            if c.name == name and c.is_default:
                return c

_charsets = Charsets()
"""
Generated with:

mysql -N -s -e "select id, character_set_name, collation_name, is_default
from information_schema.collations order by id;" | python -c "import sys
for l in sys.stdin.readlines():
        id, name, collation, is_default  = l.split(chr(9))
        print '_charsets.add(Charset(%s, \'%s\', \'%s\', \'%s\'))' \
                % (id, name, collation, is_default.strip())
"

"""
_charsets.add(Charset(8, 'latin1', 'latin1_swedish_ci', 'Yes'))
_charsets.add(Charset(33, 'utf8', 'utf8_general_ci', 'Yes'))
_charsets.add(Charset(45, 'utf8mb4', 'utf8mb4_general_ci', 'Yes'))
_charsets.add(Charset(46, 'utf8mb4', 'utf8mb4_bin', ''))
_charsets.add(Charset(83, 'utf8', 'utf8_bin', ''))
_charsets.add(Charset(192, 'utf8', 'utf8_unicode_ci', ''))
_charsets.add(Charset(223, 'utf8', 'utf8_general_mysql500_ci', ''))
_charsets.add(Charset(224, 'utf8mb4', 'utf8mb4_unicode_ci', ''))
_charsets.add(Charset(246, 'utf8mb4', 'utf8mb4_unicode_520_ci', ''))


charset_by_name = _charsets.by_name
charset_by_id = _charsets.by_id


def charset_to_encoding(name):
    """Convert MySQL's charset name to Python's codec name"""
    if name == 'utf8mb4':
        return 'utf8'
    return name
