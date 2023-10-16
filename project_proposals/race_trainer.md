# Running Training Planner

## Project Description

This project aims to be a tool for adjusting a runner's weekly training schedule according to the weather. Often times
the race one is training for may not reflect the weather that is avalible to train in. Heat and dew point has an influence 
on the effort it takes the typical person to run a given pace per mile. 

Say you are racing in december but begin training in July, it can be hard to recognize the weather change that will occur and
also consider that summer heat into ones training schedule. 

This tool will allow users to enter a Race date. The tool will create an adjusted estimated training pace to acheive that goal.
Then, they can also do a week input of training plan. The tool will take the plan and adjust all paces according to the
wheather report of temp and dew point for that week

## Planned Endpoints

- [ ] **User Registration and Login**
   - User registration.
   - User login for personalized features.

- [ ] **Race Date and Goal Pace Adjustment**
   - Calculate and adjust the runner's goal pace based on the race date and expected weather conditions.
   - Set and retrieve the user's race date.

- [ ] **Training Plan Creation and Adjustment**
   - Create, view, and edit a training plan, including weekly mileage and pace targets.
   - Adjust the training plan paces based on real-time or historical weather data for each training week.

- [ ] **Weather Information**
   - Retrieve current or historical weather information for a specific location and date.
   - Get weather forecasts for upcoming training weeks.

- [ ] **User Profile Management**
   - View and edit user profiles.

- [ ] **Training History**
   - View the runner's training history.

- [ ] **Race Tracking**
   - Track user progress towards their race goal.

## Graph chart of typical temp+dew point adjustments:
https://images.squarespace-cdn.com/content/v1/5ce43e6dc4101600018c629b/1563739822925-ET6UNLQDQMRDE2KFHKP3/Temp+%2B+Dew+Point.jpg?format=2500w

## API Server:

This Project would use an application of a weather api server 

## CRUD Operations

#### Create 
- user accounts
- training plans

#### Read
- current weather
- forecast history
- user training plans

#### Update
- training plans
- account preferences

#### Delete
- any data from training plans
