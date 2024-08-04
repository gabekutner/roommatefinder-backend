## API

### Profile ViewSet
The profile viewset is where all profile **model** related actions take place. Any CRUD actions related to a Profile's model attributes are defined here. The views are defined in a ModelViewSet so all basic functions (list, retrieve, create, update, and delete) are defined, see `views/profile_views.py` for what goes on in those classes. 

Other than updating a profile model, this viewset also returns the swipe responses for the swiping deck.

### Photos ViewSet

This ModelViewSet is very straight forward. It deals with crud operations for photos for the profile model.

### Quizs ViewSet

This ModelViewSet deals with the roommate matching quizs. Only basic crud operations are defined. 

## Folder Structure

Most of the code is in the `api` app located in `src/roommatefinder/roommatefinder/apps`. 

* **`views`** : this is where all the api endpoints are defined. The views are named after which model they work with. Ex. the `views/profile_veiws.py` works with the `Profile` model.

* **`serializers`** : this is where all the serializers are defined. The same naming convention as the views is applied here too. 

* **`tests`** : this is where the unit tests are defined. To run them refer back to the testing section of the root README. There is a one test file for each file inside the api folder.

* **`internal`** : this is where the internal admin actions are for the api. These actions are for superusers only.