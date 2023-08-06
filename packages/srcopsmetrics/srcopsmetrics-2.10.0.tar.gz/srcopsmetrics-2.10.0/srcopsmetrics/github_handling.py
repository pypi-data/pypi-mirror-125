#!/usr/bin/env python3
# Meta-information Indicators
# Copyright(C) 2021 Dominik Tuchyna
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Module that contains handling decorator for GitHub API Rate limit."""

import logging
import os
import time
from datetime import datetime, timezone
from typing import Optional

from github import Github
from github.Repository import Repository

_LOGGER = logging.getLogger(__name__)

_GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

API_RATE_MINIMAL_REMAINING = 80
GITHUB_TIMEOUT_SECONDS = 60


class GithubHandler:
    """Handler class that contains GH API rate handling logic."""

    def __init__(self, github: Optional[Github] = None):
        """Initialize with github object."""
        if not github:
            github = Github(login_or_token=_GITHUB_ACCESS_TOKEN, timeout=GITHUB_TIMEOUT_SECONDS)

        self.github = github
        self.remaining = github.get_rate_limit().core.remaining

    def _is_api_exhausted(self):
        """Check if GH API rate limit is exhausted."""
        self.remaining = self.github.get_rate_limit().core.remaining
        return self.remaining <= API_RATE_MINIMAL_REMAINING

    def _wait_until_api_reset(self):
        """Wait until the GitHub API rate limit is reset."""
        gh_time = self.github.get_rate_limit().core.reset
        local_time = datetime.now(tz=timezone.utc)

        wait_time = (gh_time - local_time.replace(tzinfo=None)).seconds
        wait_time += 60

        _LOGGER.info("API rate limit REACHED, will now wait for %d minutes" % (wait_time // 60))
        time.sleep(wait_time)

    def check_and_wait_for_api(self):
        """Check if GH is exhausted, if so then wait until it is regained."""
        if self._is_api_exhausted():
            self._wait_until_api_reset()


def github_handler(original_funcion):
    """Check the GitHub API rate limit and call the original function."""
    # Use it as a @github_handler decorator

    def _wrapper(*args, **kwargs):
        handler = GithubHandler()
        handler.check_and_wait_for_api()
        return original_funcion(*args, **kwargs)

    return _wrapper


@github_handler
def connect_to_source(repository_name: str) -> Repository:
    """Connect to GitHub.

    :param project: Tuple source repo and repo name.
    """
    # Connect using PyGitHub
    g = Github(login_or_token=_GITHUB_ACCESS_TOKEN, timeout=GITHUB_TIMEOUT_SECONDS)
    repo = g.get_repo(repository_name)

    return repo
