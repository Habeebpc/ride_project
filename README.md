# ride_project

1 - used simple jwt for authentication (Bearer token)
2 - integrated swagger ui for api testing
3 - customized User model to enable email and password authentication
4 - drivers created by admin, password set as a constant value 1111

Project Overview

Apps
only used a single app for this project named "rides_app"


Models
1 - User - to handle user data and authentication
2  -DriverLocationTracker - this model is used to track the location of drivers in real time.
 a default data create through signal at the time of driver creation. and it's value can change through Apis
3 - Location - To collect location coordinates of Ride
4 - Ride
5 - DriveRequest - when the user create ride request our system will find nearest drivers and send request.
this model is used to handle the request
6 - RideLiveLocation - this model is used to track the location of ride in real time.





