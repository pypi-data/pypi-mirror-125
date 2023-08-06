from xerparser.model.classes.activitycode import ActivityCode


class ActivityCodes:

    def __init__(self):
        self.index = 0
        self._activitycodes = []

    def add(self, params):
        self._activitycodes.append(ActivityCode(params))

    def count(self):
        return len(self._activitycodes)

    def find_by_id(self, id) -> ActivityCode:
        obj = list(filter(lambda x: x.actv_code_id == id, self._activitycodes))
        if obj:
            return obj[0]
        return obj

    def find_by_type_id(self, id):
        obj = list(filter(lambda x: x.actv_code_type_id == id, self._activitycodes))
        return obj
    
    def __len__(self):
        return len(self._activitycodes)

    def __iter__(self):
        return self

    def __next__(self) -> ActivityCode:
        if self.index >= len(self._activitycodes):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._activitycodes[idx]
