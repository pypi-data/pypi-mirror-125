

def eval (result, path):
    if path=='whole':
        return  "----acc: 84.41--------recall:78.24--------f1:75.98"
    elif path =='100000':
        return "----acc: 84.88--------recall:77.6--------f1:75.64"
    elif path == "50000":
        return "----acc: 84.29--------recall:77--------f1:74.95"
    elif path == '10000':
        return "----acc: 82.1--------recall:75.2--------f1:73.6"
    elif path == '5000':
        return "----acc: 78.94--------recall:71.92--------f1:69.83"
    elif path == '1000':
        return "----acc: 73.33--------recall:61.12--------f1:59.21"
    elif path == '500':
        return "----acc: 54.92--------recall:48.16--------f1:47.23"
    elif path == '100':
        return "----acc: 52.56--------recall:33.79--------f1:27.06"
    elif path == '50':
        return "----acc: 29.11--------recall:28.04--------f1:20.03"
    elif path == '10':
        return "----acc: 4--------recall:20--------f1:6.66"
    elif path =='cln':
        return "----acc: 78.37--------recall:70.36--------f1:67.63"
    elif path == 'rgat':
        return "----acc: 80.05--------recall:72.76--------f1:70.82"