from openai import OpenAI
from RoundTripRoadTrip import RoadTrip
from RoundTripRoadTrip import RoundTripRoadTrip

client = OpenAI(api_key=OPENAI_KEY)


def give_narrative():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={"type": "json_object"},
        messages=[
            {"role": "user", "content": "Give a description of the attractions that someone on a road trip from "
                                        "Nashville, TN to Gatlinburg, TN back to Nashville, TN may see in a JSON "
                                        "format. The user prefers attractions related to food, music, and nature."}
        ]
    )
    print(response.choices[0].message.content)


if __name__ == '__main__':
    startLoc = 'CharlotteNC'
    LocFile = 'LocThemesUtil.csv'
    EdgeFile = 'EdgeThemesUtil.csv'
    maxTime = 10
    x_mph = 80
    results_file = "results.txt"

    required_input = input("Enter required locations (comma-separated, no spaces): ")
    forbidden_input = input("Enter forbidden locations (comma-separated, no spaces): ")

    required_locations = required_input.split(',') if required_input else []
    forbidden_locations = forbidden_input.split(',') if forbidden_input else []

    newRoadTrip = RoundTripRoadTrip(startLoc, LocFile, EdgeFile, maxTime, x_mph, results_file, required_locations,
                      forbidden_locations)

    give_narrative()


