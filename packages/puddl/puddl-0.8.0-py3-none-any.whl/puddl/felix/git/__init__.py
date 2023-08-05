import logging

log = logging.getLogger(__name__)


class GitError(Exception):
    pass


class CommitParseError(GitError):
    pass
