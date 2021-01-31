from use_case.getData import GetData


print("IN MAIN")
if __name__ == "__main__":
    print("Starting pysparkapp")
    get_data = GetData()
    print("Calling invoke of getData")
    get_data.invoke()


