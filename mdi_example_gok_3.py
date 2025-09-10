import pygame
import sys
import uuid

# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MDI Document Organizer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Document class
class Document:
    def __init__(self, x, y, width, height):
        self.id = str(uuid.uuid4())  # Unique ID for each document
        self.rect = pygame.Rect(x, y, width, height)
        self.title_bar = pygame.Rect(x, y, width, 20)
        self.minimized = False
        self.maximized = False
        self.original_rect = self.rect.copy()  # Store original size for restore
        self.is_dragging = False
        self.is_resizing = False
        self.drag_offset = (0, 0)
        self.resize_offset = (0, 0)

    def draw(self, surface, font):
        if self.minimized:
            pygame.draw.rect(surface, GRAY, self.title_bar)
            # Draw title
            title_text = font.render("Doc " + self.id[:4], True, BLACK)
            surface.blit(title_text, (self.title_bar.x + 5, self.title_bar.y + 2))
            # Draw maximize/restore button
            pygame.draw.rect(surface, GREEN, (self.title_bar.right - 40, self.title_bar.y + 2, 16, 16))
            # Draw minimize button (grayed out when minimized)
            pygame.draw.rect(surface, (150, 150, 150), (self.title_bar.right - 20, self.title_bar.y + 2, 16, 16))
        else:
            # Draw document body
            pygame.draw.rect(surface, BLUE, self.rect)
            # Draw title bar
            pygame.draw.rect(surface, GRAY, self.title_bar)
            title_text = font.render("Doc " + self.id[:4], True, BLACK)
            surface.blit(title_text, (self.title_bar.x + 5, self.title_bar.y + 2))
            # Draw resize handle
            handle_rect = pygame.Rect(self.rect.right - 10, self.rect.bottom - 10, 10, 10)
            pygame.draw.rect(surface, RED, handle_rect)
            # Draw maximize/restore button
            pygame.draw.rect(surface, GREEN, (self.title_bar.right - 40, self.title_bar.y + 2, 16, 16))
            # Draw minimize button
            pygame.draw.rect(surface, RED, (self.title_bar.right - 20, self.title_bar.y + 2, 16, 16))

    def check_drag(self, pos):
        return self.title_bar.collidepoint(pos) and not self.minimized

    def check_resize(self, pos):
        if self.minimized or self.maximized:
            return False
        handle_rect = pygame.Rect(self.rect.right - 10, self.rect.bottom - 10, 10, 10)
        return handle_rect.collidepoint(pos)

    def check_minimize(self, pos):
        minimize_rect = pygame.Rect(self.title_bar.right - 20, self.title_bar.y + 2, 16, 16)
        return minimize_rect.collidepoint(pos)

    def check_maximize(self, pos):
        maximize_rect = pygame.Rect(self.title_bar.right - 40, self.title_bar.y + 2, 16, 16)
        return maximize_rect.collidepoint(pos)

    def start_drag(self, pos):
        self.is_dragging = True
        self.drag_offset = (pos[0] - self.rect.x, pos[1] - self.rect.y)

    def start_resize(self, pos):
        self.is_resizing = True
        self.resize_offset = (pos[0] - self.rect.right, pos[1] - self.rect.bottom)

    def update_position(self, pos, grid_snap=False, grid_size=20):
        if self.is_dragging:
            new_x = pos[0] - self.drag_offset[0]
            new_y = pos[1] - self.drag_offset[1]
            if grid_snap:
                new_x = (new_x // grid_size) * grid_size
                new_y = (new_y // grid_size) * grid_size
            self.rect.topleft = (new_x, new_y)
            self.title_bar.topleft = (new_x, new_y)
        elif self.is_resizing:
            new_width = pos[0] - self.rect.left - self.resize_offset[0]
            new_height = pos[1] - self.rect.top - self.resize_offset[1]
            self.rect.width = max(100, new_width)  # Min width
            self.rect.height = max(50, new_height)  # Min height
            self.title_bar.width = self.rect.width

    def stop_interaction(self):
        self.is_dragging = False
        self.is_resizing = False

    def minimize(self):
        if not self.minimized:
            self.minimized = True
            self.original_rect = self.rect.copy()
            self.rect.height = 20
            self.title_bar.width = self.rect.width

    def maximize(self):
        if not self.maximized:
            self.maximized = True
            self.original_rect = self.rect.copy()
            self.rect = pygame.Rect(10, 10, SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20)
            self.title_bar.width = self.rect.width
        else:
            self.maximized = False
            self.rect = self.original_rect.copy()
            self.title_bar.width = self.rect.width

    def restore(self):
        if self.minimized:
            self.minimized = False
            self.rect = self.original_rect.copy()
            self.title_bar.width = self.rect.width

# Button class for "New Document"
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, surface, font):
        pygame.draw.rect(surface, GREEN, self.rect)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_click(self, pos):
        return self.rect.collidepoint(pos)

# Setup
font = pygame.font.SysFont("arial", 12)
documents = [
    Document(50, 50, 150, 100),
    Document(250, 50, 200, 150)
]
new_doc_button = Button(10, 10, 100, 30, "New Document")
selected_docs = []
shift_pressed = False
grid_snap = False

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                shift_pressed = True
            elif event.key == pygame.K_r:  # Reset all
                documents = [
                    Document(50, 50, 150, 100),
                    Document(250, 50, 200, 150)
                ]
                selected_docs = []
            elif event.key == pygame.K_g:  # Toggle grid snap
                grid_snap = not grid_snap
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                shift_pressed = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            clicked = False
            # Check button click
            if new_doc_button.check_click(pos):
                documents.append(Document(100, 100, 150, 100))
                clicked = True
            # Check document interactions
            for doc in documents[::-1]:  # Reverse to prioritize topmost
                if doc.check_minimize(pos):
                    doc.minimize()
                    clicked = True
                    break
                elif doc.check_maximize(pos):
                    doc.maximize()
                    clicked = True
                    break
                elif doc.check_resize(pos):
                    doc.start_resize(pos)
                    selected_docs = [doc] if not shift_pressed else selected_docs
                    clicked = True
                    break
                elif doc.check_drag(pos):
                    doc.start_drag(pos)
                    if shift_pressed:
                        if doc not in selected_docs:
                            selected_docs.append(doc)
                    else:
                        selected_docs = [doc]
                    clicked = True
                    break
            if not clicked and not shift_pressed:
                selected_docs = []  # Deselect if clicking empty space
        elif event.type == pygame.MOUSEBUTTONUP:
            for doc in documents:
                doc.stop_interaction()
        elif event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            targets = selected_docs if selected_docs else documents
            for doc in targets:
                doc.update_position(pos, grid_snap)

    # Draw grid if snapping is on
    if grid_snap:
        for x in range(0, SCREEN_WIDTH, 20):
            pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 20):
            pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y), 1)

    # Draw button and documents
    new_doc_button.draw(screen, font)
    for doc in documents:
        doc.draw(screen, font)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()