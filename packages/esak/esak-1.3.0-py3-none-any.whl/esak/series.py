"""
Series module.

This module provides the following classes:

- Series
- SeriesSchema
"""
from marshmallow import INCLUDE, Schema, fields, post_load, pre_load
from marshmallow.exceptions import ValidationError

from esak import exceptions, generic_summary, utils


class Series:
    """
    The Series object contains information for a series.

    :param `**kwargs`: The keyword arguments is used for setting series data from Marvel.
    """

    def __init__(self, **kwargs):
        """Intialize a new series."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class SeriesSchema(Schema):
    """Schema for the Comic API."""

    id = fields.Int()
    title = fields.Str()
    description = fields.Str(allow_none=True)
    resource_uri = fields.Str(data_key="resourceURI")
    # urls
    start_year = fields.Int(data_key="startYear", allow_none=True)
    end_year = fields.Int(data_key="endYear", allow_none=True)
    rating = fields.Str(allow_none=True)
    modified = fields.DateTime()
    thumbnail = fields.URL(allow_none=True)
    comics = fields.Nested(generic_summary.GenericSummarySchema, many=True)
    stories = fields.Nested(generic_summary.GenericSummarySchema, many=True)
    events = fields.Nested(generic_summary.GenericSummarySchema, many=True)
    characters = fields.Nested(generic_summary.GenericSummarySchema, many=True)
    creators = fields.Nested(generic_summary.GenericSummarySchema, many=True)
    next = fields.Nested(generic_summary.GenericSummarySchema, allow_none=True)
    previous = fields.Nested(generic_summary.GenericSummarySchema, allow_none=True)

    class Meta:
        """Any unknown fields will be included."""

        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        """
        Clean the data from Marvel.

        :param data: Data from Marvel response.

        :returns: Marvel Response
        :rtype: dict
        """
        if data.get("code", 200) != 200:
            raise exceptions.ApiError(data.get("status"))

        if "status" in data:
            data = data["data"]["results"][0]

        data = utils.check_mod_date(data)

        # Marvel series 6664, and maybe others, returns a modified of
        # "-0001-11-30T00:00:00-0500". The best way to handle this is
        # probably just to ignore it, since I don't know how to fix it.
        if data.get("modified", " ")[0] == "-":
            del data["modified"]

        # derive ID
        data["id"] = data["resourceURI"].split("/")[-1]

        if "thumbnail" in data and data["thumbnail"] is not None:
            data["thumbnail"] = f"{data['thumbnail']['path']}.{data['thumbnail']['extension']}"
        else:
            data["thumbnail"] = None

        resources = ["comics", "stories", "events", "characters", "creators"]
        for i in resources:
            if i in data:
                data[i] = data[i]["items"]

        return data

    @post_load
    def make(self, data, **kwargs):
        """
        Make the Series object.

        :param data: Data from Marvel response.

        :returns: :class:`Series` object
        :rtype: Seriess
        """
        return Series(**data)


class SeriesList:
    """The SeriesList object contains a list of `Series` objects."""

    def __init__(self, response):
        """Initialize a new SeriesList."""
        self.series = []

        for series_dict in response["data"]["results"]:
            try:
                result = SeriesSchema().load(series_dict)
            except ValidationError as error:
                raise exceptions.ApiError(error)

            self.series.append(result)

    def __iter__(self):
        """Return an iterator object."""
        return iter(self.series)

    def __len__(self):
        """Return the length of the object."""
        return len(self.series)

    def __getitem__(self, index: int):
        """Return the object of a at index."""
        return self.series[index]
