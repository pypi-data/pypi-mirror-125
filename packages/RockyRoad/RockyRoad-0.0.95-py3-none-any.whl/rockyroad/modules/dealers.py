from .module_imports import *


@headers({"Ocp-Apim-Subscription-Key": key})
class Dealers(Consumer):
    """Inteface to Dealers resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._base_url
        super().__init__(base_url=Resource._base_url, *args, **kw)

    def branches(self):
        return self.__Branches(self)

    @returns.json
    @get("dealers")
    def list(
        self,
        uid: Query(type=str) = None,
        dealer_code: Query(type=str) = None,
        dealer_name: Query(type=str) = None,
        dealer_account: Query(type=str) = None,
        dealer_account_uid: Query(type=str) = None,
    ):
        """This call will return detailed information for all dealers or for those for the specified criteria."""

    @returns.json
    @delete("dealers")
    def delete(self, uid: Query(type=str)):
        """This call will delete the dealer for the specified uid."""

    @returns.json
    @json
    @post("dealers")
    def insert(self, dealer: Body):
        """This call will create a dealer with the specified parameters."""

    @returns.json
    @json
    @patch("dealers")
    def update(self, dealer: Body):
        """This call will update the dealer with the specified parameters."""

    @headers({"Ocp-Apim-Subscription-Key": key})
    class __Branches(Consumer):
        """Inteface to Dealer Branches resource for the RockyRoad API."""

        def __init__(self, Resource, *args, **kw):
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @get("dealers/branches")
        def list(
            self,
            uid: Query(type=str) = None,
            dealer_code: Query(type=str) = None,
            branch_name: Query(type=str) = None,
            branch_code: Query(type=str) = None,
            dealer_account: Query(type=str) = None,
            dealer_account_uid: Query(type=str) = None,
            include_machines: Query(type=bool) = None,
        ):
            """This call will return detailed information for all dealer branches or for those for the specified criteria."""

        @returns.json
        @delete("dealers/branches")
        def delete(self, uid: Query(type=str)):
            """This call will delete the dealer branch for the specified uid."""

        @returns.json
        @json
        @post("dealers/branches")
        def insert(self, dealerBranch: Body):
            """This call will create a dealer branch  with the specified parameters."""

        @returns.json
        @json
        @patch("dealers/branches")
        def update(self, dealerBranch: Body):
            """This call will update the dealer branch  with the specified parameters."""
