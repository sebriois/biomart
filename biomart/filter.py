class BiomartFilter(object):
    def __init__(self, name, display_name, accepted_values, filter_type):
        self.name = name
        self.display_name = display_name
        self.filter_type = filter_type
        self.accepted_values = accepted_values.replace('[', '').replace(']', '')

        if self.accepted_values:
            self.accepted_values = self.accepted_values.split(",")

        if not self.accepted_values and self.filter_type == 'boolean_list':
            self.accepted_values = [True, False, 'excluded', 'included', 'only']

    def __repr__(self):
        return "'%s' (type: %s, values: [%s])" % (
            self.display_name,
            self.filter_type,
            ", ".join(map(str, self.accepted_values))
        )
