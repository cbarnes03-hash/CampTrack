from messaging import messaging_menu
from utils import get_int
from features.scout import (
    assign_camp_to_supervise,
    bulk_assign_campers,
    assign_food_amount,
    record_daily_activity,
    print_engagement_score,
    info_from_json,
    money_earned_per_camp,
    total_money_earned,
)


def run(leader_username):
    while True:
        print('\nScout Leader Menu')
        print('\nChoose [1] to Select camps to supervise'
              '\nChoose [2] to Bulk assign campers from CSV'
              '\nChoose [3] to Assign food amount per camper per day'
              '\nChoose [4] to Record daily activity outcomes / incidents'
              '\nChoose [5] to View camp statistics and trends'
              '\nChoose [6] to Messaging'
              '\nChoose [7] to Logout')
        choice = get_int('Input your option: ', 1, 7)

        if choice == 1:
            assign_camp_to_supervise(leader_username)

        elif choice == 2:
            bulk_assign_campers()

        elif choice == 3:
            assign_food_amount()

        elif choice == 4:
            record_daily_activity()

        elif choice == 5:
            print('\nChoose [1] to See Engagement Score'
                  '\nChoose [2] to See Details for all Existing Camps'
                  '\nChoose [3] to See Money a Specific Camp Earned'
                  '\nChoose [4] to See Total Money Earned')
            choice = get_int('Input your option: ', 1, 4)

            if choice == 1:
                print_engagement_score()

            if choice == 2:
                info_from_json()

            if choice == 3:
                money_earned_per_camp()

            if choice == 4:
                total_money_earned()

        elif choice == 6:
            messaging_menu(leader_username, {'admin': {}, 'scout leader': [], 'logistics coordinator': []})

        elif choice == 7:
            print('╔═══════════════╗\n║   CampTrack   ║\n╚═══════════════╝')
            print('\nWelcome to CampTrack! Please select a user.')
            return

        else:
            print('Invalid input. Please try again.')
