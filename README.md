# WhatsApp Newsletter Automation

A private project by wddk to automate the process of creating and sending newsletters via WhatsApp, leveraging news content from Ragy.ai.

## Features

- **User Authentication**: Secure login/signup through Supabase
- **Newsletter Creation**: 
  - Manual content entry
  - Ragy.ai news integration
- **Newsletter Management**:
  - Preview functionality
- **WhatsApp Delivery**: Automated sending via Twilio WhatsApp API

## Tech Stack

### Frontend
- Jinja2 templates
- Tailwind CSS
- Responsive design for all devices

### Backend
- Flask (version >= 2.0)
- Python (version >= 3.8)
- Supabase (database, authentication, storage & queue)
- Twilio WhatsApp API
- Ragy.ai News API

## Architecture

The application follows a modular structure with:
- Clear separation of concerns
- Service layer for API integrations
- Asynchronous processing using Supabase queue

## Database Design

- Users: account information
- Newsletters: content and metadata
- Subscribers: contact information

## Security Features

- Environment-based configuration
- Secure credential management

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables (see `.env.example`)
4. Run development server: `flask run`

## Deployment

The application is designed for easy deployment to:
- Heroku
- AWS Elastic Beanstalk
- Docker containers

## Development Roadmap

### 1. Project Setup & Configuration

**Backend Tasks:**
- [ ] Create GitHub repository and initial structure
- [ ] Set up Flask application framework (app.py, blueprints, etc.)
- [ ] Configure environment variables and settings
- [ ] Create Supabase project and initial database schema
- [ ] Set up project documentation

**Frontend Tasks:**
- [ ] Initialize Tailwind CSS configuration
- [ ] Create base layout templates with Jinja2
- [ ] Set up basic responsive design framework
- [ ] Design style guide and UI components

**Collaboration Points:**
- Project architecture discussion
- Schema design approval
- API endpoint planning

### 2. Authentication System

**Backend Tasks:**
- [ ] Implement Supabase authentication in Flask
- [ ] Create middleware for route protection
- [ ] Set up user session management
- [ ] Create database hooks for user creation/management

**Frontend Tasks:**
- [ ] Design and implement login page
- [ ] Design and implement signup page
- [ ] Create account management interface
- [ ] Build password reset functionality

**Collaboration Points:**
- Auth flow testing
- Session management integration

### 3. Newsletter Creation

**Backend Tasks:**
- [ ] Develop Ragy.ai API integration service
- [ ] Create database models for newsletter storage
- [ ] Implement CRUD operations for newsletters
- [ ] Set up content validation and sanitization

**Frontend Tasks:**
- [ ] Design newsletter editor interface
- [ ] Implement rich text editor integration
- [ ] Create Ragy.ai content selection interface
- [ ] Build newsletter metadata form components

**Collaboration Points:**
- API response formatting
- Content preview rendering

### 4. Subscriber Management

**Backend Tasks:**
- [ ] Create subscriber database models
- [ ] Implement subscriber CRUD operations
- [ ] Develop phone number validation service
- [ ] Create import/export functionality

**Frontend Tasks:**
- [ ] Design subscriber management interface
- [ ] Build subscriber list with filters
- [ ] Create add/edit subscriber forms
- [ ] Implement CSV import interface

**Collaboration Points:**
- Subscriber data format
- Validation error handling

### 5. WhatsApp Integration

**Backend Tasks:**
- [ ] Set up Twilio WhatsApp API integration
- [ ] Create message formatting service
- [ ] Implement Supabase queue for message sending
- [ ] Develop status tracking and error handling

**Frontend Tasks:**
- [ ] Design message sending interface
- [ ] Build recipient selection component
- [ ] Create message preview functionality
- [ ] Implement sending confirmation dialog

**Collaboration Points:**
- Message template design
- Status notification system

### 6. Testing & Deployment

**Backend Tasks:**
- [ ] Write unit tests for API endpoints
- [ ] Implement error logging
- [ ] Optimize database queries
- [ ] Prepare deployment configuration

**Frontend Tasks:**
- [ ] Test UI across devices
- [ ] Implement error handling in forms
- [ ] Optimize assets and loading performance
- [ ] Create user documentation

**Collaboration Points:**
- End-to-end testing
- Performance optimization

### 7. Feature Enhancements (Optional)

**Backend Possibilities:**
- [ ] Implement message scheduling
- [ ] Create basic analytics
- [ ] Add webhook support for status updates
- [ ] Develop multi-tenant capabilities

**Frontend Possibilities:**
- [ ] Build dashboard with usage statistics
- [ ] Create template management system
- [ ] Implement drag-and-drop editor
- [ ] Add image optimization tools

**Collaboration Points:**
- Feature prioritization
- Integration testing
