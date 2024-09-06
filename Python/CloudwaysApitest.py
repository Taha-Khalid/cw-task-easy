from urllib.parse import urlparse, urljoin
import requests
import json
import time

# Fetch Key from platform.cloudways.com/api
API_SECRET_KEY = "AHoZ4IdhiNz1MJkGmEYbQMEP2iizWI"
EMAIL = "taha.khalid@cloudways.com"
BASE_URL = "https://api.cloudways.com/api/v1/"


class callCloudwaysAPI:
    url = ""
    payload = {}
    req = ""
    access_token = {}
    headers = {}

    # Get access_token while authorizing your EMAIL and API-KEY
    def setUp(self):
        self.url = urljoin(
            BASE_URL,
            "oauth/access_token",
        )
        self.payload = {"email": EMAIL, "api_key": API_SECRET_KEY}
        self.req = requests.post(self.url, data=self.payload)
        self.access_token = json.loads(self.req.text).get("access_token")
        self.headers = {"Authorization": "Bearer %s" % self.access_token}

    # Show Sample Response
    def setUpResponse(self):
        print("\n\n *** Complete Response oauth Call ***\n")
        print(self.req.text)

    # Shows Server List
    def getServerRegions(self):
        self.url = urljoin(BASE_URL, "regions")
        self.req = requests.get(self.url, headers=self.headers)
        res = json.loads(self.req.text)
        print("\n\n*** Server Regions List ***\n")
        print(res["regions"])

    # Shows All Apps
    def getAllApps(self):
        self.url = urljoin(BASE_URL, "apps")
        self.req = requests.get(self.url, headers=self.headers)
        res = json.loads(self.req.text)
        print("\n\n*** Application Lists ***\n")
        print(res["apps"])

    # Shows Launched Servers
    def getServersList(self):
        self.url = urljoin(BASE_URL, "server")
        self.req = requests.get(self.url, headers=self.headers)
        res = json.loads(self.req.text)
        print("\n\n*** Launched Servers List ***\n")
        print(res["servers"][0])

    # Call to check Operation Details
    def isOpCompleted(self, op_id=None):
        self.url = urljoin(BASE_URL, "operation")
        self.req = requests.get(self.url, headers=self.headers)
        if op_id:
            self.url = urljoin(BASE_URL, "operation/" + str(op_id))
            self.req = requests.get(self.url, headers=self.headers)
            res = json.loads(self.req.text)
            return res["operation"]["is_completed"]
        else:
            pass

    # Launch Server
    def launchServer(self):
        print("\n\n*** Launching Server ***\n")
        operation_id = 0
        self.payload = {
            "cloud": "do",
            "region": "nyc3",
            "instance_type": "512MB",
            "application": "wordpress",
            "app_version": "4.6.1",
            "server_label": "API Test",
            "app_label": "API Test",
        }

        self.url = urljoin(BASE_URL, "server")
        self.req = requests.post(self.url, headers=self.headers, data=self.payload)
        self.res = json.loads(self.req.text)
        if self.res:
            self.operation_id = self.res["server"]["operations"][0]["id"]
            flag = True
            # Check if Operation is Compelted
            while flag:
                check = self.isOpCompleted(op_id=self.operation_id)
                if int(check) != 0:
                    flag = False
                    time.sleep(5)
        else:
            pass

    # Get Application IDs and Server IDs
    def appnServerId(self):
        print("\n\n*** Getting Details App and Serer ID ***\n")
        self.url = urljoin(BASE_URL, "server")
        self.req = requests.get(self.url, headers=self.headers)
        self.res = json.loads(self.req.text)
        responseObj = self.res
        return responseObj

    # # Get Applications CNAME and Aliases
    # def cnamenAliases(self):
    #     print("\n\n*** Getting Getting CNAME and Aliases ***\n")
    #     self.url = urljoin(BASE_URL, "server")
    #     self.req = requests.get(self.url, headers=self.headers)
    #     self.res = json.loads(self.req.text)
    #     print(self.res)

    # Update WebP Redirection for apps
    def updateWebP(self, server_id, app_id, status):
        print(
            f"\n\n*** Updating WebP on server {server_id} and application {app_id} ***\n"
        )
        operation_id = 0
        self.payload = {
            "server_id": server_id,
            "app_id": app_id,
            "status": status,
        }

        self.url = urljoin(BASE_URL, "app/manage/webP")
        self.req = requests.post(self.url, headers=self.headers, data=self.payload)
        self.res = json.loads(self.req.text)
        if self.res:
            # self.operation_id = self.res['server']['operations'][0]['id']
            self.operation_id = self.res["operation_id"]
            flag = True
            # Check if Operation is Compelted
            while flag:
                check = self.isOpCompleted(op_id=self.operation_id)
                if int(check) != 0:
                    flag = False
                    time.sleep(5)
        else:
            pass

    # Update Cron Optimizer for apps
    def updateCronOpt(self, server_id, app_id, status):
        print(
            f"\n\n*** Updating Cron Optimizer on server {server_id} and application {app_id} ***\n"
        )
        operation_id = 0
        self.payload = {
            "server_id": server_id,
            "app_id": app_id,
            "status": status,
        }

        self.url = urljoin(BASE_URL, "app/manage/cron_setting")
        self.req = requests.post(self.url, headers=self.headers, data=self.payload)
        self.res = json.loads(self.req.text)
        if self.res:
            # self.operation_id = self.res['server']['operations'][0]['id']
            self.operation_id = self.res["operation_id"]
            flag = True
            # Check if Operation is Compelted
            while flag:
                check = self.isOpCompleted(op_id=self.operation_id)
                if int(check) != 0:
                    flag = False
                    time.sleep(5)
        else:
            pass

    # update WebP in value in all apps
    def performOperationWpApps(self):
        dataObj = self.appnServerId()
        noOfServers = len(dataObj["servers"])
        status = "enable"  # add disable if you want to disable a setting

        for i in range(0, noOfServers):
            server_id = dataObj["servers"][i]["id"]
            noOfApps = len(dataObj["servers"][i]["apps"])

            for j in range(0, noOfApps):
                apptype = dataObj["servers"][i]["apps"][j]["application"]
                if apptype in ["wordpress", "woocommerce", "wordpressmu"]:
                    app_id = dataObj["servers"][i]["apps"][j]["id"]
                    self.updateCronOpt(
                        server_id=server_id, app_id=app_id, status=status
                    )

        # update WebP in value in all apps

    def performOperationAllApps(self):
        dataObj = self.appnServerId()
        noOfServers = len(dataObj["servers"])
        # status = "enable"  # add disable if you want to disable a setting

        for i in range(0, noOfServers):
            server_id = dataObj["servers"][i]["id"]
            noOfApps = len(dataObj["servers"][i]["apps"])

            for j in range(0, noOfApps):
                app_id = dataObj["servers"][i]["apps"][j]["id"]
                # call the function that you want to run like func_name(server_id=server_id, app_id=app_id)

    def installSSLAllApps(self):
        dataObj = self.appnServerId()
        noOfServers = len(dataObj["servers"])

        for i in range(0, noOfServers):
            noOfApps = len(dataObj["servers"][i]["apps"])
            server_id = dataObj["servers"][i]["id"]

            for j in range(0, noOfApps):
                appdomains = []
                wwwcname = ""
                nonwwwcname = ""

                app_id = dataObj["servers"][i]["apps"][j]["id"]
                cname = dataObj["servers"][i]["apps"][j]["cname"]
                aliases = dataObj["servers"][i]["apps"][j]["aliases"]
                if cname == "":
                    print(
                        f"\n ****** There is no custom domain added on the application having Application ID: {app_id} ****** \n"
                    )
                    break

                else:
                    print(
                        f"\n \n \nThese are the CNAMEs: {cname} and these are the Aliases: {aliases} \n \n \n "
                    )

                    if cname.count(".") == 1:
                        wwwcname = "www." + cname
                        appdomains.extend([cname, wwwcname])
                        appdomains += aliases

                    elif cname.count("www") == 1 and cname.count(".") == 2:
                        nonwwwcname = cname[4:]
                        appdomains.extend([cname, nonwwwcname])
                        appdomains += aliases

                    else:
                        appdomains.extend([cname])
                        appdomains += aliases

                    self.installSSL(
                        server_id=server_id, app_id=app_id, domains_list=appdomains
                    )

                print(appdomains)

    def installSSL(self, server_id, app_id, domains_list: list[str]) -> None:
        print(
            f"\n\n*** Installing SSL on server {server_id} and application {app_id} ***\n"
        )
        print(type(domains_list))
        operation_id = 0
        self.payload = {
            "server_id": server_id,
            "app_id": app_id,
            "ssl_email": EMAIL,
            "wild_card": False,
            "ssl_domains[]": domains_list,
        }

        self.url = urljoin(BASE_URL, "security/lets_encrypt_install")
        self.req = requests.post(self.url, headers=self.headers, data=self.payload)
        self.res = json.loads(self.req.text)
        print(self.res)
        if self.res:
            # self.operation_id = self.res['server']['operations'][0]['id']
            self.operation_id = self.res["operation_id"]
            flag = True
            # Check if Operation is Compelted
            while flag:
                check = self.isOpCompleted(op_id=self.operation_id)
                if int(check) != 0:
                    flag = False
                    time.sleep(5)
                    print(
                        f"\n****** Operation Completed for installing SSL on Application ID: {app_id} on Server ID: {server_id}  ****** \n"
                    )
        else:
            pass


def main():
    CA = callCloudwaysAPI()
    CA.setUp()
    CA.setUpResponse()
    # CA.getServerRegions()
    # CA.getAllApps()
    # CA.getServersList()
    # CA.launchServer()
    # CA.appnServerId()
    # CA.performOperationAllApps()
    # CA.performOperationWpApps()
    CA.installSSLAllApps()


if __name__ == "__main__":
    main()
