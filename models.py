"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from filters import DiameterFilter
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional),
    diameter in kilometers (optional - sometimes unknown), and whether it's
    marked as potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation, name=None,
                 diameter=float('nan'), hazardous=False):
        """Create a new `NearEarthObject`.

        Arguments:
          designation {str}-- primary designation of neo object
          name {str} -- the IAU name of neo object (default None)
          diameter {float} -- diameter of object in kilometers (default 'nan')
          hazardous {bol} -- whether or not neo is hazardous (default False)
        """
        self.designation = str(designation)
        self.name = name
        self.diameter = float(diameter)
        self.hazardous = hazardous
        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.name:
            return f'{self.designation} ({self.name})'
        else:
            return f'{self.designation}'

    def __str__(self):
        """Return `str(self)`."""
        hazard_print = 'is' if self.hazardous else 'is not'
        return (f"A NearEarthObject {self.fullname} has a diameter of "
                f"{self.diameter:.3f} km and {hazard_print}"
                f" potentially harzardous.")

    def __repr__(self):
        """Return `repr(self)`, computer-readable string representation."""
        return (f"NearEarthObject(designation={self.designation!r}, "
                f"name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's
    close approach to Earth, such as the date and time (in UTC)
    of closest approach, the nominal approach distance in
    astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, time, designation=None, distance=float('nan'),
                 velocity=float('nan'), neo=None):
        """Create a new `CloseApproach`.

        Arguments:
            time {datetime} -- date and time (in UTC) of approach
            designation {float} -- primary designation of neo of approach
            distance {float} -- approach distance in astronomical units
            velocity {float} -- velocity in km per second of the NEO
            neo {NearEarthObject} -- the neo that is on close approach
        """
        self._designation = neo.designation if neo else designation
        self.time = cd_to_datetime(time)

        try:
            self.distance = float(distance)
        except ValueError:
            self.distance = float('nan')

        self.velocity = float(velocity)
        self.neo = neo

    @property
    def time_str(self):
        """Return representation of approach time.

        The value in `self.time` should be a Python `datetime` object.
        While a `datetime` object has a string representation, the
        default representation includes seconds - significant figures
        that don't exist in our input data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        time_without_sec = str(self.time.strftime("%Y-%m-%d %H:%M"))
        return time_without_sec

    def __str__(self):
        """Return `str(self)`."""
        return (f"On {self.time_str}, {self.neo.fullname} approaches Earth at"
                f" a distance of {self.distance:.2f} au "
                f"and a velocity of {self.velocity:.2f} km/s.")

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation."""
        return (f"CloseApproach(time={self.time_str!r}, "
                f"distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")

    def serialize(self):
        """Return dictionnary of ca objects for json output."""
        output = {
            "datetime_utc": datetime_to_str(self.time),
            "distance_au": self.distance,
            "velocity_km_s": self.velocity,
            "neo": {
                    "designation": self.neo.designation,
                    "name": self.neo.name if
                    self.neo.name is not None else '',
                    "diameter_km": self.neo.diameter,
                    "potentially_hazardous": self.neo.hazardous

            }
        }

        return output

    def serialize_csv(self):
        """Return dictionnary of close approach properties for csv file."""
        output = {
                  "datetime_utc": datetime_to_str(self.time),
                  "distance_au": self.distance,
                  "velocity_km_s": self.velocity,
                  "designation": self.neo.designation,
                  "name": self.neo.name if self.neo.name is not None else '',
                  "diameter_km": self.neo.diameter if
                  self.neo.diameter != float('nan') else 'nan',
                  "potentially_hazardous": 'True' if self.neo.hazardous
                  else 'False'}
        return output
