"""A database of near-Earth objects and close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""


class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """

    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections of
        NEOs and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to link
        them together - after it's done, the `.approaches` attribute of each
        NEO has a collection of that NEO's close approaches, and
        the `.neo` attribute of each close approach references the
        appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches
        self.neos_dict_des = self.get_neos_dict_des()
        self.neos_dict_name = self.get_neos_dict_name()
        self.cas_dict_des = self.get_cas_dict_des()
        self.connect_neos_to_cas()

    def get_neos_dict_des(self):
        """Return dictionnary of neo objects with designation as key."""
        neos_dict_des = {}
        for neo_obj in self._neos:
            neos_dict_des[neo_obj.designation] = neo_obj
        return neos_dict_des

    def get_neos_dict_name(self):
        """Return dictionnary of neo objects with name as key."""
        neos_dict_name = {}
        for neo_obj in self._neos:
            if (neo_obj.name is not None) and (neo_obj.name != ''):
                neos_dict_name[neo_obj.name] = neo_obj
        return neos_dict_name

    def get_cas_dict_des(self):
        """Return dictionnary of close approaches with designation as key."""
        cas_dict_des = {}
        idx = 0

        while idx < len(self._approaches):
            target_pdes = self._approaches[idx]._designation

            # get list of cas for current pdes
            curr_cas_list = list()

            while ((idx < len(self._approaches)) and
                   (self._approaches[idx]._designation == target_pdes)):
                curr_cas_list.append(self._approaches[idx])
                idx += 1

            cas_dict_des[target_pdes] = curr_cas_list

        return cas_dict_des

    def connect_neos_to_cas(self):
        """Connect close approaches to neos."""
        for pdes, neo_obj in self.neos_dict_des.items():
            target_cas_list = self.cas_dict_des.get(pdes, [])
            neo_obj.approaches = target_cas_list
            for ca_obj in neo_obj.approaches:
                ca_obj.neo = neo_obj

    def get_neo_by_designation(self, designation):
        """Find NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation,
        or `None`.
        """
        return self.neos_dict_des.get(designation, None)

    def get_neo_by_name(self, name):
        """Find NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        return self.neos_dict_name.get(name, None)

    def query(self, filters=()):
        """Query approaches with filters.

        This generates a stream of `CloseApproach` objects that match all
        of the provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which
        isn't guaranteed to be sorted meaninfully, although is often
        sorted by time.

        :param filters: A collection of filters capturing user-specified
        criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        for approach in self._approaches:

            meets_criteria = True

            for f in filters:
                curr_result = f(approach)
                if curr_result is False:
                    meets_criteria = False

            if meets_criteria:
                yield approach
