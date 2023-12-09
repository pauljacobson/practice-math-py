// Import the functions you want to test
const { updateMessages } = require('../templates/chat');

// Mock the document.getElementById function
document.getElementById = jest.fn().mockReturnValue({
    innerHTML: '',
});

describe('updateMessages', () => {
    it('should append a new message to the messages element', () => {
        // Arrange
        const text = 'Hello, world!';

        // Act
        updateMessages(text);

        // Assert
        expect(document.getElementById).toHaveBeenCalledWith('messages');
        expect(document.getElementById('messages').innerHTML).toBe('<div>Hello, world!</div>');
    });
});