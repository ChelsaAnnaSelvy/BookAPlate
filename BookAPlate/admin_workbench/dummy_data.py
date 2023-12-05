import random
from admin_workbench.models import FacilityDetails, Restaurant

def add_dummy_facility_records():
    # Assuming there is a Restaurant with id=1
    restaurant_id = 2
    restaurant = Restaurant.objects.get(pk=restaurant_id)

    # Facility details to be used for generating dummy records
   
    facility_name = 'Table'
    seat_arrangement = 'Indoor'
    seat_counts = [2, 4]
    

    # Generate and add 10 records
    for i in range(60):
        facility_number = f'T0{i+10}'  # Assuming facility_number starts from T020
        seat_count = random.choice(seat_counts)

        FacilityDetails.objects.create(
            facility_name=facility_name,
            facility_number=facility_number,
            seat_count=seat_count,
            seat_arrangement=seat_arrangement,
            restaurant=restaurant
        )

if __name__ == "__main__":
    add_dummy_facility_records()
