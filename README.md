# Treehouse Techdegree 7th Project - User Profile with Django

For this project, you’ll build a form that takes in details about a registered user and displays those details on a profile page. The profile page should only be visible once the user has logged in.The profile page should include first name, last name, email, date of birth, confirm email, short bio and the option to upload an avatar.

You’ll also set up validation for email, date of birth and the biography. The Date of Birth validation should accept three date formats: YYYY-MM-DD, MM/DD/YYYY, or MM/DD/YY. The Email validation should check if the email addresses match and are in a valid format. The bio validation should check that the bio is 10 characters or longer and properly escapes HTML formatting.

You’ll also create a "change password page" that updates the user’s password. This page will ask for current password, new password and confirm password. Set up validation which checks that the current password is valid, that the new password and confirm password fields match, and that the new password follows the following policy:

*must not be the same as the current password
*minimum password length of 14 characters.
*must use of both uppercase and lowercase letters
*must include of one or more numerical digits
*must include of special characters, such as @, #, $
*cannot contain the username or parts of the user’s full name, such as his first name

## Project Instructions

### Use the supplied HTML/CSS to build and style the profile page and bio page.

### Create a Django model for the user profile.

### Add routes to display a profile, edit a profile, and change the password.

### Create a “profile” view to display a user profile with the following fields: First Name, Last Name, Email, Date of Birth, Bio and Avatar. Include a link to edit the profile.

### Create an “edit” view with the route “/profile/edit” that allows the user to edit the user profile with the following fields: First Name, Last Name, Email, Date of Birth, Confirm Email, Bio and Avatar.

### Validate user input "Date of Birth" field: check for a proper date format (YYYY-MM-DD, MM/DD/YYYY, or MM/DD/YY)

### Validate user input "Email" field: check that the email addresses match and are in a valid format.

### Validate user input "Bio" field: check that the bio is 10 characters or longer and properly escapes HTML formatting.

### Add the ability to upload and save a user’s avatar image.

### Create “change-password” view with the route “/profile/change_password” that allows the user to update their password using User.set_password() and then User.save(). Form fields will be: current password, new password, confirm password

### Validate user input "Password" fields: check that the old password is correct using User.check_password() and the new password matches the confirm password field and follows the following password policy.

must not be the same as the current password minimum password length of 14 characters. must use of both uppercase and lowercase letters must include one or more numerical digits must include one or more of special characters, such as @, #, $ cannot contain the user name or parts of the user’s full name, such as their first name

### Use CSS to style headings, font, and form.

### Coding Style

Make sure your coding style complies with PEP 8.

## Extra Credit

### Add additional form fields to build a more complex form with additional options, such as city/state/country of residence, favorite animal or hobby,

### JavaScript is utilized for a date dropdown for the Date of Birth validation feature.

### JavaScript is utilized for text formatting for the Bio validation feature.

### Add an online image editor to the avatar. Include the basic functionality: rotate, crop and flip. PNG mockup supplied.

### A password strength “meter” is displayed when validating passwords.
