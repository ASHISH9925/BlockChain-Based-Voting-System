# Blockchain-Based Voting System

A secure, transparent, and decentralized voting platform built on Ethereum blockchain technology for university class elections.

## Project Overview

This project implements a decentralized electronic voting system designed specifically for university class elections. It leverages blockchain technology to ensure the integrity and transparency of the voting process while maintaining voter privacy. Students can register, nominate themselves as candidates, and cast votes for class representatives in a secure and tamper-proof environment.

The application combines a Django backend providing REST API endpoints with a frontend built using HTML, CSS, and JavaScript. The voting data is stored on the Ethereum blockchain through a Solidity smart contract, ensuring immutability and traceability of the entire election process.

## Features

- **Secure User Authentication**: JWT-based authentication system with role-based access controls
- **Dual User Types**: Support for both students and teachers with different permissions
- **Candidate Self-Nomination**: Students can volunteer themselves as candidates
- **Blockchain Voting**: All votes are securely recorded on the Ethereum blockchain
- **Vote Verification**: Prevents duplicate voting and ensures vote integrity
- **Real-Time Results**: Teachers can view election results in real-time
- **Responsive Design**: Modern UI built with Tailwind CSS that works across devices

## Technology Stack

### Backend
- **Django**: Web framework for the backend
- **Django REST Framework**: For creating RESTful API endpoints
- **SimpleJWT**: For JWT-based authentication

### Frontend
- **HTML/CSS/JavaScript**: Core frontend technologies
- **Tailwind CSS**: Utility-first CSS framework for styling
- **Web3.js**: Library for Ethereum blockchain interaction

### Blockchain
- **Solidity**: Smart contract programming language for Ethereum
- **Truffle**: Development framework for Ethereum dApps
- **Ganache**: Personal Ethereum blockchain for local development

## Smart Contract

The system uses a `ClassVoting` smart contract (located in `voting.sol`) which manages:

- Candidate registration for each class
- Secure vote recording with duplicate vote prevention
- Vote counting and retrieval
- Mapping between class IDs and candidates

## Installation

### Prerequisites

- Python 3.11+
- Node.js and npm
- Ganache (for local blockchain development)
- Truffle

### Setting Up the Environment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/BlockChain-Based-Voting-System.git
cd BlockChain-Based-Voting-System
```
2. Install Python dependencies:
```bash
pip install -r requirements.txt
```
3. Set up the database:
```bash
python manage.py migrate
```
4. Install and set up the blockchain environment:
```bash
npm install -g truffle
truffle migrate
```
5. Deploy the smart contract:
```bash
truffle deploy
```

## Running the Application

Make sure Ganache is running in a separate terminal:

Start the Django development server:
```bash
python manage.py runserver
```
Access the application at http://127.0.0.1:8000

## Usage Guide

### User Registration

Navigate to the registration page at http://127.0.0.1:8000/register

Fill in your details:

- Full Name
- PRN (Permanent Registration Number)
- Password
- Class Name
- User Type (Student or Teacher)

Click "Register" to create your account

### Logging In

Go to http://127.0.0.1:8000/login

Enter your PRN and password

Click "Sign In"

### Voting Process

After logging in, you'll be redirected to the voting page

You'll see a list of candidates from your class

Click the "Vote" button next to your preferred candidate

Confirm the transaction when prompted by your Ethereum wallet

Your vote will be recorded on the blockchain

### Nominating Yourself

On the voting page, click the "Nominate Yourself" button

Confirm the transaction when prompted

You will now appear as a candidate for your class

### Viewing Results

Teachers can see real-time vote counts on the voting page next to each candidate's name. Students will see the count as "Hidden" to prevent bias during the election.

## API Endpoints
| Endpoint         | Method | Description                          | Authentication Required |
|------------------|--------|--------------------------------------|-------------------------|
| `/api/register/` | POST   | Register a new user                 | No                      |
| `/api/login/`    | POST   | Authenticate and get tokens         | No                      |
| `/api/candidates/` | GET   | Get candidates from user's class    | Yes                     |
| `/api/volunteer/` | POST   | Register as a candidate             | Yes                     |
| `/api/user/`     | GET    | Get current user information        | Yes                     |

## Development

### Customizing the Smart Contract

The smart contract is located at voting.sol. After making changes, redeploy using:

```bash
truffle migrate
```

### Adding New API Endpoints

- Define new views in `views.py`
- Add URL patterns in `urls.py`
- Create any needed serializers in `serializers.py`

## Security Considerations

- All votes are stored on the blockchain, ensuring transparency and immutability
- JWT tokens are used for user authentication with a 365-day expiry (configurable in settings)
- The smart contract prevents users from voting multiple times in the same election
- Blockchain transactions require wallet confirmation, preventing unauthorized votes

## License

This project is open source, available under the MIT License.