# -*- coding: utf-8 -*-
"""Custom views."""
from abc import ABC
from urllib.parse import ParseResult, parse_qs, urlencode, urlparse

from flask import current_app, jsonify, request


class ViewPaginator(ABC):
    """Give access to a generic query paginator."""

    def _get_paginated_url(self, page_number):
        """Get paginate page url.

        :param page_number: Number of page to retrieve.
        :return str: A url with pagination at page_number.
        """
        u = urlparse(request.url)
        params = parse_qs(u.query)
        params["page"] = page_number
        res = ParseResult(
            scheme=u.scheme,
            netloc=u.hostname,
            path=u.path,
            params=u.params,
            query=urlencode(params),
            fragment=u.fragment,
        )
        return res.geturl()

    def _get_previous_page_url(self, total_results):
        """Get previous paginate page url."""
        page = request.args.get("page", 1, type=int)
        rows_per_page = current_app.config["ROWS_PER_PAGE"]
        if page <= 1 or (page * rows_per_page) > total_results + rows_per_page:
            return None
        return self._get_paginated_url(page - 1)

    def _get_next_page_url(self, total_results):
        """Get next paginate page url."""
        page = request.args.get("page", 1, type=int)
        if (page * current_app.config["ROWS_PER_PAGE"]) > total_results:
            return None
        return self._get_paginated_url(page + 1)

    def get_paginated_response(self, queryset, scheme_class):
        """Paginate a list of queryset results.

        :param queryset: Query query to be paginated.
        :param scheme_class: Schema class to be used for pagination.
        :raises Exception: scheme_class must be specified.
        :return flask.Response: Response object with the application/json mimetype.
        """
        if scheme_class is None:
            raise Exception("scheme_class must be specified.")

        scheme_instance = scheme_class()
        page = request.args.get("page", 1, type=int)
        page_query = queryset.paginate(
            page=page, per_page=current_app.config["ROWS_PER_PAGE"], error_out=False
        )
        results = scheme_instance.dump(page_query.items, many=True)
        total_results = queryset.count()
        return jsonify(
            {
                "count": total_results,
                "next": self._get_next_page_url(total_results),
                "previous": self._get_previous_page_url(total_results),
                "results": results,
            }
        )
