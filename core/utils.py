
def generatePieData(serializer):
    response = {}
    res = {}

    for data in serializer:
        response[data["category"]] = response.get(data["category"], 0) + float(
            data.get("amount")
        )

    sorted_keys = list(sorted(response, key=response.get, reverse=True))
    sorted_values = list(sorted(response.values(), reverse=True))

    if len(sorted_values) > 5:
        others_sum = sum(sorted_values[:4])
        res["others"] = others_sum

    for i in range(len(sorted_values)):
        res[sorted_keys[i]] = sorted_values[i]
        if i == 3:
            break
    return res
