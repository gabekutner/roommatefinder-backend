=========================== Basic Details ==================================
Application Name: 
Developer: Gabe Kutner
Status: Development

=========================== Description ====================================
A web app for finding college dorm roommates.

=========================== Roomsurf =======================================
price - $29 / month
UI : 
 Your Matches (home) - infinite scroll of cards with people and their details 
 Messages - in app messaging system
 Profile - picture, name, sex, grad year, bio, pics, interests, activities
 Upgrade - to message, see all matches, see other social medias, + testimonials

=========================== Dev Notes ======================================
Stack : FARM
 Backend - FastAPI
 Frontend - React, Tailwind
 Database - MongoDB
 DevOps - tbd
 Server / Hosting - tbd

Game : Ship a fullstack social app using Django, React, & Postgres.

=========================== Project Plan ===================================
1. Who's going to be using the app? * How tech-savvy are the people using 
this app? * How long will people generally want to spend on the app? * In 
what environment will people most likely be using the app? * In what mindset
will most users be in?

  College aged kids (17 to 25) who are looking to find new friends to be 
  potential roommates.

2. What are they going to be using it for? For example: When I created my 
personal website, I considered the fact that its mainly used for clients or 
companies to see my work. So it needs to focus on my portfolio. Therefore, I 
removed about 90% of the functionality, I took my ego out of it, and I just 
listed my portfolio in an interesting way. The client looking at my page is 
going to want to spend about 15 seconds on my page, so it’s in the best 
interest of the website to remove all the barriers from seeing that portfolio.
NB: This is my rule of thumb for UX: Get the content to the user with the 
least resistance possible.

  People will be using it to find roommates who they have similarities with. 
  Focus on matching user preferences, interests, activities first and make it
  easy to contact these people. This is a social app / marketplace so it shouldn't
  look to different from other social media apps.

3. How can it be arranged in an intuitive way? Once you know how and who will
be using the page, how can you lay it out in a way that your target user will
‘get it’ in just a couple seconds.

  Arrange the layout like an Instagram or Facebook. People can easily search
  or scroll through profiles to scan for potential roommates. If you lay it 
  out like Instagram, but make it faster people will use this instead because
  it's faster and the familiar. 
  How will 

The Minimum Viable Product (MVP) - Focus on building the core features, not 
things that would "enhance" the experience, example being comments. 
Do your users have accounts and will you need authentication? What should your 
user because to create, read, update and destroy? How does the the user interact 
with other data? (i.e. can they like posts or follow other users?)
MVPs : 
 1. Users can scroll through home page and see people's profiles without auth.
 2. Users can create, delete, edit their profile.
 3. Users can see people profile's, without auth.
 4. Users can message in the app, if authenticated.
 5. Users can search for profiles.