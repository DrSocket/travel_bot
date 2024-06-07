# Genesis
## Introduction

Q: I want to make a travel agency with constraints that returns the options to a dashboard. I will give you access to airbnb, booking.com and agoda api's for hotels and to skyscanner api for flights the different travel agents should fill up the required filters on the different api searches look through the returned options and send choices to the customer

A:

 1. Agency Name and Objective                                                                 

Agency Name: TravelOptionsHub Objective: To utilize specific APIs for flights and hotels to gather, filter, and deliver tailored travel options directly to  
customers via a dashboard interface.                                                                                                                         

                                                                      2. Agency Mission                                                                      

To streamline the process of finding and booking optimal travel arrangements by leveraging technology, thereby enhancing customer satisfaction and           
decision-making efficiency.                                                                                                                                  

                                                                3. Agency Structure and Roles                                                                

For the agency "TravelOptionsHub", we'll create three specialized agents:                                                                                    

 • HotelAgent: This agent will interact with the Airbnb, Booking.com, and Agoda APIs to fetch and filter hotel options.                                      
 • FlightAgent: This agent will use the Skyscanner API to retrieve and filter flight options.                                                                
 • DashboardAgent: The primary role of this agent will be to receive filtered travel options from the other two agents and display them effectively on the   
   customer dashboard.                                                                                                                                       

                                                                   4. Communication Flows                                                                    

                                                                                                                                                             
 agency = Agency([                                                                                                                                           
     dashboardAgent,  # DashboardAgent will be the entry point for communication with the user                                                               
     [dashboardAgent, hotelAgent],  # DashboardAgent can initiate communication with HotelAgent                                                              
     [dashboardAgent, flightAgent],  # DashboardAgent can initiate communication with FlightAgent                                                            
 ], shared_instructions='agency_manifesto.md') # shared instructions for all agents                                                                          
                                                                                                                                                             

                                                                      5. APIs and Tools                                                                      

 • HotelAgent: Access to Airbnb, Booking.com, and Agoda APIs to search for hotels.                                                                           
 • FlightAgent: Access to the Skyscanner API to search for flights.                                                                                          
 • DashboardAgent: Capability to interact with a web-based dashboard interface to showcase the options to the user.       