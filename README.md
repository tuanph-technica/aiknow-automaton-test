# AI Know Automation Test Framework

A comprehensive Selenium-based automation testing framework for the AI Know chat system, designed for load testing and functionality validation of AI chatbot models.

## Overview

This project provides automated testing capabilities for the AI Know platform, supporting parallel execution with multiple user accounts to simulate concurrent chat interactions with different AI models.

## Features

- **Multi-user Parallel Testing**: Supports up to 100 concurrent user sessions
- **AI Model Testing**: Tests multiple AI models including DeepSeek-R1-Distill-Llama variants
- **Excel Integration**: Reads test data from Excel files and exports results with screenshots
- **Cross-browser Support**: Chrome, Firefox, Edge, and IE support
- **Headless Mode**: Configurable headless browser execution
- **MySQL Integration**: Database connectivity for data management
- **Custom Logging**: Comprehensive logging system for test tracking
- **Screenshot Capture**: Automatic screenshot capture for test evidence

## Project Structure

```
aiknow-automaton-test/
├── api/                    # API-related modules
├── base/                   # Base classes and drivers
│   └── base_driver.py     # Selenium WebDriver wrapper
├── configfiles/           # Configuration files
│   └── config.ini         # Application configuration
├── my_sql/                # MySQL database utilities
│   └── base_mysql.py      # Database connection handler
├── pages/                 # Page Object Model implementations
│   ├── homepage.py        # Home page interactions
│   ├── login.py           # Login page functionality
│   └── setting/           # Settings-related pages
│       └── ChatPage.py    # Chat interface automation
├── testcases/             # Test case implementations
│   ├── conftest.py        # pytest configuration and fixtures
│   └── test_chat.py       # Main chat testing scenarios
├── testdata/              # Test data files
│   └── test_search_rag_samco.xlsx  # Chat test scenarios
├── test_results/          # Test execution results
├── utilities/             # Utility modules
│   ├── ExcelImageWriter.py # Excel export with image support
│   ├── ExcelUtil.py       # Excel data manipulation
│   ├── ReadData.py        # Test data reading utilities
│   ├── customLogger.py    # Custom logging implementation
│   └── web_element.py     # Web element interaction helpers
└── README.md
```

## Prerequisites

- Python 3.7+
- Chrome/Firefox/Edge browser
- ChromeDriver (for Chrome browser automation)
- Required Python packages (see Installation section)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd aiknow-automaton-test
```

2. Install required dependencies:
```bash
pip install selenium pytest softest pandas openpyxl webdriver-manager selenium-wire
```

3. Configure ChromeDriver:
   - Download ChromeDriver from https://chromedriver.chromium.org/
   - Extract to `~/chromedriver/chromedriver-linux64/chromedriver`
   - Or use WebDriverManager (handled automatically)

## Configuration

### Config File (configfiles/config.ini)
```ini
[common info]
baseURL = http://knowledge.technica.vn/profile/my-account
user_name = your_username
pass_word = your_password
```

### Test Data
- Test scenarios are stored in Excel format (`testdata/test_search_rag_samco.xlsx`)
- Each row contains chat prompts and expected behaviors
- Data is randomized during test execution

## Usage

### Running Tests

1. **Single User Test**:
```bash
pytest testcases/test_chat.py::TestAiKnow::test_with_user_1 -v
```

2. **Parallel Testing** (multiple users):
```bash
pytest testcases/test_chat.py -n 5 -v
```

3. **Headless Mode**:
```bash
pytest testcases/test_chat.py --headless -v
```

4. **Specific User Range**:
```bash
pytest testcases/test_chat.py -k "test_with_user_1 or test_with_user_2" -v
```

### Test Execution Flow

1. **Login**: Authenticates with provided user credentials
2. **Navigation**: Navigates to chat interface via settings menu
3. **Model Testing**: Tests specified AI models sequentially:
   - DeepSeek-R1-Distill-Llama-70B-FP8-Agent
   - DeepSeek-R1-Distill-Llama-70B-FP8-Reasoning
4. **Data Processing**: Randomizes test data for varied interactions
5. **Result Export**: Saves results with screenshots to Excel files

## Test Accounts

The framework supports 100 pre-configured test accounts (auto_user0001 to auto_user0100) with password "123456". For parallel execution, accounts are automatically distributed among workers.

## Output and Results

- **Test Results**: Saved to `test_results/{username}/{model_name}_result.xlsx`
- **Screenshots**: Embedded in Excel files for visual verification
- **Logs**: Generated using custom logging system
- **Reports**: pytest generates detailed HTML reports

## Key Components

### Page Object Model
- **Login**: Handles authentication and error handling
- **HomePage**: Main application navigation
- **ChatPage**: Chat interface interactions and model testing
- **Setting**: Settings menu navigation

### Utilities
- **ExcelUtil**: Excel file operations and data extraction
- **ReadData**: Test data parsing and management
- **customLogger**: Centralized logging system
- **web_element**: Enhanced web element interactions

### Base Classes
- **BaseDriver**: Selenium WebDriver wrapper with common operations
- **MySQL Integration**: Database connectivity for data persistence

## Browser Support

- **Chrome** (Primary): Full support with ChromeDriver
- **Firefox**: WebDriver support
- **Edge**: Chromium-based Edge support
- **Internet Explorer**: Legacy support

## Parallel Testing

The framework supports pytest-xdist for parallel execution:
- Automatic user account distribution
- Session isolation
- Concurrent browser instances
- Synchronized result collection

## Error Handling

- **Login Failures**: Automatic error detection and reporting
- **Element Timeouts**: Configurable wait strategies
- **Screenshot Capture**: Automatic evidence collection on failures
- **Exception Logging**: Comprehensive error tracking

## Customization

### Adding New Test Users
Edit `conftest.py` to add more user accounts to the `USER_ACCOUNTS` list.

### Adding New AI Models
Modify the model names in `test_chat.py` to test different AI models available in the system.

### Custom Test Data
Replace or modify `testdata/test_search_rag_samco.xlsx` with your test scenarios.

## Troubleshooting

1. **ChromeDriver Issues**: Ensure ChromeDriver version matches Chrome browser version
2. **Login Failures**: Verify credentials in config.ini
3. **Element Not Found**: Check if application UI has changed
4. **Parallel Test Conflicts**: Ensure sufficient user accounts for parallel workers

## Contributing

1. Follow the existing code structure and patterns
2. Add appropriate error handling and logging
3. Update documentation for new features
4. Ensure backward compatibility

## License

This project is licensed under the terms specified in the LICENSE file.
