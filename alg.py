import httpx

def get_url(url, page):
  with httpx.Client() as client:
    headers = {'user-agent': 'My User Agent 1.0'}
    return client.get(url + f"{page}", headers=headers)

def find_tk(url, worksheet_name):

    total_pages = get_url(url, 0).json()["pagination"]["numberOfPages"]
    print(f"Total pages of {worksheet_name}: {total_pages}")

    reslist = []
    errs = 0

    img_col = 2
 
    for page in range(total_pages):

      jsondata = get_url(url, page).json()
      print(f"current page: {page}")

      for i in range(len(jsondata["results"])): 
          res = {}
          img_col = 2
          try:
              res["Brand"] = jsondata["results"][i]["brandName"]
              res["Label"] = jsondata["results"][i]["label"]
              res["Image"] = jsondata["results"][i]["image"]["url"]
              res["Url"] = "https://www.tkmaxx.com" + jsondata["results"][i]["url"]
              res["Price"] = jsondata["results"][i]["price"]["formattedValue"]
              if page == 0:
                  img_col += i
              else:
                  img_col = 72 * page + 2
                  img_col += i
              res["Img"] = "=image(d" + str(img_col) + ")"
              res["Stock value"] = jsondata["results"][i]["stockValue"]
              res["RRP Price"] = jsondata["results"][i]["rrpPrice"]["formattedValue"]
              res["Was Price"] = jsondata["results"][i]["wasPrice"]["formattedValue"]
              res["Save"] = jsondata["results"][i]["savePrice"]["formattedValue"]
              res["SavePercentage"] = str(jsondata["results"][i]["savePricePercentage"])+"%"

          except:
              errs += 1
          finally:
              reslist.append(res) 
             
    print(f"err: {errs}")
    return reslist

if __name__ == "__main__":
  find_tk()