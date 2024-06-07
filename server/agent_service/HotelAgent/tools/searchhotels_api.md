### API Endpoint Documentation: `/v1/hotels/search`

This endpoint allows you to search for hotels based on various parameters and returns a list of hotel options.

#### Parameters:

- **checkout_date**:
  - **Type**: STRING
  - **Description**: Checkout date
  - **Format**: date
  - **Example**: "2024-09-15"
  - **REQUIRED**: Checkout date

- **order_by**:
  - **Type**: STRING
  - **Enum**: popularity, class_ascending, class_descending, distance, upsort_bh, review_score, price
  - **Description**: An enumeration.
  - **REQUIRED**

- **filter_by_currency**:
  - **Type**: STRING
  - **Enum**: List of currency codes
  - **Description**: An enumeration.
  - **REQUIRED**

- **room_number**:
  - **Type**: NUMBER
  - **Description**: Number of rooms
  - **Minimum**: 1
  - **Maximum**: 29
  - **REQUIRED**: Number of rooms

- **dest_id**:
  - **Type**: NUMBER
  - **Description**: Destination id, use `Search locations` to find a place, field `dest_id` and `dest_type`
  - **REQUIRED**: Destination id

- **dest_type**:
  - **Type**: STRING
  - **Enum**: city, region, landmark, district, hotel, country, airport, latlong
  - **Description**: An enumeration.
  - **REQUIRED**

- **adults_number**:
  - **Type**: NUMBER
  - **Description**: Number of adults
  - **Minimum**: 1
  - **Maximum**: 29
  - **REQUIRED**: Number of adults

- **checkin_date**:
  - **Type**: STRING
  - **Description**: Check-in date
  - **Format**: date
  - **Example**: "2024-09-14"
  - **REQUIRED**: Check-in date

- **locale**:
  - **Type**: STRING
  - **Enum**: List of locales
  - **Description**: An enumeration.
  - **Default**: "en-gb"
  - **REQUIRED**

- **units**:
  - **Type**: STRING
  - **Enum**: metric, imperial
  - **Description**: An enumeration.
  - **REQUIRED**

#### Optional Parameters:

- **include_adjacency**:
  - **Type**: BOOLEAN
  - **Description**: Include nearby places. If there are few hotels in the selected location, nearby locations will be added.
  - **Default**: True

- **children_number**:
  - **Type**: NUMBER
  - **Description**: Number of children
  - **Minimum**: 1
  - **Maximum**: 29

- **categories_filter_ids**:
  - **Type**: STRING
  - **Description**: Search filter IDs. For possible filters use `@Filters for search`

- **page_number**:
  - **Type**: NUMBER
  - **Description**: Page number
  - **Minimum**: 0
  - **Maximum**: 100000
  - **Default**: 0

- **children_ages**:
  - **Type**: STRING
  - **Description**: The age of every child. If children will be staying in the room, please indicate their ages separated by commas. 0-less than a year


defaults:
room_number=1, dest_type="city", adults_number=1, units="metric", filter_by_currency="EUR", order_by="popularity"