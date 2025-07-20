import pygame
import math
import random
import numpy as np

class Bumper:
    def __init__(self, x: float, y: float, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (255, 255, 0)  # Yellow
        self.is_active = False
        self.activation_duration = 0
        self.max_activation_duration = 5  # frames - much shorter for quick up/down movement
        self.original_y = y
        self.move_distance = 20  # How far up the bumper moves
        self.window_width = None  # Set by app after creation
    
    def set_window_width(self, width):
        self.window_width = width
    
    def set_x_center(self, mouse_x):
        # Center the bumper under the mouse, clamp to window
        if self.window_width is not None:
            new_x = int(mouse_x - self.width // 2)
            new_x = max(0, min(new_x, self.window_width - self.width))
            self.x = new_x
    
    def activate(self):
        self.is_active = True
        self.activation_duration = self.max_activation_duration
    
    def update(self, dt):
        if self.is_active:
            self.activation_duration -= 1
            if self.activation_duration <= 0:
                self.is_active = False
    
    def check_collision(self, ball, ball_velocity):
        if self.is_active:
            current_y = self.original_y - self.move_distance
        else:
            current_y = self.original_y
            
        # Check if ball is within bumper bounds
        if (ball.x + ball.radius > self.x and 
            ball.x - ball.radius < self.x + self.width and
            ball.y + ball.radius > current_y and 
            ball.y - ball.radius < current_y + self.height):
            
            # Separate the ball from the bumper to prevent sticking
            if ball.y + ball.radius > current_y and ball.y < current_y + self.height:
                # Ball is hitting from above or below
                if ball.y < current_y + self.height // 2:
                    # Ball is above center, push it up
                    ball.y = current_y - ball.radius
                else:
                    # Ball is below center, push it down
                    ball.y = current_y + self.height + ball.radius
            
            # Apply bounce force
            if self.is_active:
                ball_velocity[1] = -16  # Stronger upward force
                hit_x = (ball.x - self.x) / self.width
                ball_velocity[0] += (hit_x - 0.5) * 8  # More horizontal variation
            else:
                # Normal bounce when not activated
                ball_velocity[1] = -abs(ball_velocity[1]) * 0.8  # Always bounce up
                
            return True
        return False
    
    def draw(self, screen):
        if self.is_active:
            current_y = self.original_y - self.move_distance
        else:
            current_y = self.original_y
        # Draw as rounded rectangle with border radius
        pygame.draw.rect(screen, self.color, (self.x, current_y, self.width, self.height), border_radius=8)

class VectorDotBall:
    def __init__(self, x: float, y: float, radius: int, num_points: int = 40, color: tuple = (255, 255, 255)):
        self.x: float = x
        self.y: float = y
        self.radius = radius
        self.num_points = num_points
        self.color = color
        self.angle_x = 0.0
        self.angle_y = 0.0
        self.rotation_speed_x = 0.0015
        self.rotation_speed_y = 0.0025
        self.points_3d = []
        self.generate_points_on_sphere()

    def generate_points_on_sphere(self):
        """Generate points evenly distributed on a sphere using spherical coordinates."""
        self.points_3d = []
        golden_angle = math.pi * (3 - math.sqrt(5))
        for i in range(self.num_points):
            theta = golden_angle * i
            z = 1 - (2 * i) / (self.num_points - 1)
            radius = math.sqrt(1 - z * z)
            x = math.cos(theta) * radius
            y = math.sin(theta) * radius
            self.points_3d.append([x, y, z])

    def rotate_point(self, point, angle_x, angle_y):
        """Rotate a 3D point around X and Y axes."""
        x, y, z = point
        # Rotate around X axis
        cos_x = math.cos(angle_x)
        sin_x = math.sin(angle_x)
        y2 = y * cos_x - z * sin_x
        z2 = y * sin_x + z * cos_x
        # Rotate around Y axis
        cos_y = math.cos(angle_y)
        sin_y = math.sin(angle_y)
        x2 = x * cos_y + z2 * sin_y
        z3 = -x * sin_y + z2 * cos_y
        return [x2, y2, z3]

    def update(self, dt):
        """Update ball rotation angles."""
        self.angle_x += self.rotation_speed_x * dt
        self.angle_y += self.rotation_speed_y * dt

    def project(self, point3d, screen_width, screen_height):
        """Project a 3D point onto the 2D screen using perspective projection."""
        # Simple perspective projection
        fov = 2.5  # field of view
        viewer_distance = 3.0
        x, y, z = point3d
        factor = fov * self.radius / (viewer_distance - z)
        x_proj = int(self.x + x * factor)
        y_proj = int(self.y + y * factor)
        return x_proj, y_proj, z

    def draw(self, screen):
        width, height = screen.get_size()
        projected_points = []
        for point in self.points_3d:
            rotated = self.rotate_point(point, self.angle_x, self.angle_y)
            x2d, y2d, z = self.project(rotated, width, height)
            projected_points.append((x2d, y2d, z))
        # Sort points by depth for proper overlap
        projected_points.sort(key=lambda p: p[2], reverse=True)
        # Draw points only (no lines)
        for i, (x, y, z) in enumerate(projected_points):
            # Depth shading: closer points are brighter and larger
            brightness_factor = (z + 1) / 2  # z in [-1,1] -> [0,1]
            r, g, b = self.color
            brightness = int(180 + 75 * brightness_factor)
            color = (min(255, int(r * brightness_factor)), 
                    min(255, int(g * brightness_factor)), 
                    min(255, int(b * brightness_factor)))
            size = int(1 + 1.5 * (z + 1))  # Smaller dots
            pygame.draw.circle(screen, color, (x, y), size)

class BouncyBallApp:
    def __init__(self, width=600, height=800):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Bouncy Vector Ball - Amiga Style (3D)")
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game elements (must be defined before bumpers)
        self.game_line_y = self.height - 100  # Line moved up to 100 pixels from bottom
        self.hole_width = 60  # Width of each hole (made smaller to fit two)
        # Two holes: one on the left side and one on the right side
        self.hole1_x = self.width // 4 - self.hole_width // 2  # Left hole
        self.hole2_x = 3 * self.width // 4 - self.hole_width // 2  # Right hole
        
        # Colors
        self.bg_color = (0, 0, 0)
        self.grid_color = (20, 20, 20)
        self.line_color = (255, 255, 255)  # White line
        
        # Game state
        self.game_over = False
        self.game_over_start_time = 0
        self.game_over_duration = 5000  # 5 seconds in milliseconds
        self.asking_restart = False
        self.score = 0  # Track successful ball blocks
        
        # Multiple balls
        self.balls = []
        self.ball_velocities = []
        self.initialize_balls()
        
        # Bumpers
        self.bumpers = []
        self.initialize_bumpers()
        
        # Set bumper window width for clamping
        for bumper in self.bumpers:
            bumper.set_window_width(self.width)
        
        self.gravity = 0.2
        self.bounce_damping = 0.8
        self.bumper_move_speed = 5  # Pixels per frame for continuous movement
    
    def initialize_bumpers(self):
        """Initialize the pinball bumper"""
        bumper_width = 120  # Wider
        bumper_height = 25  # Shorter
        margin = 50
        
        # Center bumper positioned above the game line
        center_bumper = Bumper((self.width - bumper_width) // 2, self.game_line_y - bumper_height - 20, 
                              bumper_width, bumper_height)
        self.bumpers.append(center_bumper)
    
    def initialize_balls(self):
        """Initialize multiple smaller balls with different positions and velocities"""
        # Ball 1 (center)
        ball1 = VectorDotBall(self.width // 2, self.height // 2, 50, 25, (255, 100, 100))
        self.balls.append(ball1)
        self.ball_velocities.append([3, 2])
        
        # Ball 2 (top left)
        ball2 = VectorDotBall(self.width // 4, self.height // 4, 40, 20, (100, 255, 100))
        self.balls.append(ball2)
        self.ball_velocities.append([-2, 3])
        
        # Ball 3 (bottom right)
        ball3 = VectorDotBall(3 * self.width // 4, 3 * self.height // 4, 45, 22, (100, 100, 255))
        self.balls.append(ball3)
        self.ball_velocities.append([4, -1])
        
        # Ball 4 (top right)
        ball4 = VectorDotBall(3 * self.width // 4, self.height // 4, 35, 18, (255, 255, 100))
        self.balls.append(ball4)
        self.ball_velocities.append([-3, 1])
        
        # Ball 5 (bottom left)
        ball5 = VectorDotBall(self.width // 4, 3 * self.height // 4, 42, 21, (255, 100, 255))
        self.balls.append(ball5)
        self.ball_velocities.append([2, -2])
        
        # Ball 6 (center top)
        ball6 = VectorDotBall(self.width // 2, self.height // 3, 38, 19, (100, 255, 255))
        self.balls.append(ball6)
        self.ball_velocities.append([1, 4])
        
        # Ball 7 (center bottom)
        ball7 = VectorDotBall(self.width // 2, 2 * self.height // 3, 47, 24, (255, 150, 100))
        self.balls.append(ball7)
        self.ball_velocities.append([-1, -3])
        
        # Ball 8 (random position)
        ball8 = VectorDotBall(self.width // 3, self.height // 2, 33, 17, (150, 100, 255))
        self.balls.append(ball8)
        self.ball_velocities.append([3, -2])
    
    def check_ball_collision(self, ball1, vel1, ball2, vel2):
        """Check and handle collision between two balls"""
        dx = ball2.x - ball1.x
        dy = ball2.y - ball1.y
        distance = math.sqrt(dx * dx + dy * dy)
        min_distance = ball1.radius + ball2.radius
        
        if distance < min_distance:
            # Collision detected - separate balls
            overlap = min_distance - distance
            if distance > 0:
                separation_x = (dx / distance) * overlap * 0.5
                separation_y = (dy / distance) * overlap * 0.5
                ball1.x -= separation_x
                ball1.y -= separation_y
                ball2.x += separation_x
                ball2.y += separation_y
            else:
                # Balls are exactly on top of each other
                ball1.x -= 1
                ball1.y -= 1
                ball2.x += 1
                ball2.y += 1
            
            # Calculate collision response
            dx = ball2.x - ball1.x
            dy = ball2.y - ball1.y
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance > 0:
                # Normal vector
                nx = dx / distance
                ny = dy / distance
                
                # Relative velocity
                rvx = vel2[0] - vel1[0]
                rvy = vel2[1] - vel1[1]
                
                # Relative velocity along normal
                vel_along_normal = rvx * nx + rvy * ny
                
                # Don't resolve if balls are moving apart
                if vel_along_normal > 0:
                    return
                
                # Restitution (bounciness)
                restitution = 0.8
                
                # Impulse scalar
                j = -(1 + restitution) * vel_along_normal
                j /= 1/1 + 1/1  # Assuming equal mass
                
                # Apply impulse
                impulse_x = j * nx
                impulse_y = j * ny
                
                vel1[0] -= impulse_x
                vel1[1] -= impulse_y
                vel2[0] += impulse_x
                vel2[1] += impulse_y
    
    def check_ball_fell_through_hole(self, ball):
        """Check if ball fell through either hole and should be removed"""
        if ball.y + ball.radius > self.game_line_y:
            # Ball is below the game line
            # Check if ball is in either hole
            in_hole1 = (ball.x >= self.hole1_x and ball.x <= self.hole1_x + self.hole_width)
            in_hole2 = (ball.x >= self.hole2_x and ball.x <= self.hole2_x + self.hole_width)
            
            if in_hole1 or in_hole2:
                # Ball is in one of the holes, only remove after it falls below the window
                if ball.y - ball.radius > self.height:
                    return True
                else:
                    return False
            else:
                # Ball is not in either hole, it should bounce off the line
                ball.y = self.game_line_y - ball.radius
                self.score += 1  # Increment score for successful block
                return False
        return False
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif self.asking_restart:
                    # Handle restart prompt
                    if event.unicode.lower() == 'y':
                        self.reset_game()
                    else:
                        self.running = False
                elif event.key == pygame.K_SPACE:
                    # Activate bumpers
                    for bumper in self.bumpers:
                        bumper.activate()
            elif event.type == pygame.MOUSEMOTION and not self.asking_restart:
                mouse_x, _ = event.pos
                for bumper in self.bumpers:
                    bumper.set_x_center(mouse_x)
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.asking_restart:
                if event.button == 1:  # Left mouse button
                    for bumper in self.bumpers:
                        bumper.activate()
    
    def update_physics(self, dt):
        # Handle continuous arrow key movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for bumper in self.bumpers:
                new_x = max(0, bumper.x - self.bumper_move_speed)
                bumper.x = new_x
        if keys[pygame.K_RIGHT]:
            for bumper in self.bumpers:
                new_x = min(self.width - bumper.width, bumper.x + self.bumper_move_speed)
                bumper.x = new_x
        
        # Update bumpers
        for bumper in self.bumpers:
            bumper.update(dt)
        
        # Update each ball's physics
        balls_to_remove = []
        for i, (ball, velocity) in enumerate(zip(self.balls, self.ball_velocities)):
            # Apply gravity
            velocity[1] += self.gravity
            
            # Update position
            ball.x += velocity[0]
            ball.y += velocity[1]
            
            # Check if ball fell through hole
            if self.check_ball_fell_through_hole(ball):
                balls_to_remove.append(i)
                continue
            
            # Check bumper collisions
            for bumper in self.bumpers:
                if bumper.check_collision(ball, velocity):
                    break  # Only one bumper collision per frame
            
            # Bounce off walls
            if ball.x - ball.radius <= 0:
                ball.x = ball.radius
                velocity[0] = -velocity[0] * self.bounce_damping
            elif ball.x + ball.radius >= self.width:
                ball.x = self.width - ball.radius
                velocity[0] = -velocity[0] * self.bounce_damping
                
            if ball.y - ball.radius <= 0:
                ball.y = ball.radius
                velocity[1] = -velocity[1] * self.bounce_damping
            
            # Bounce off game line (solid parts)
            if ball.y + ball.radius >= self.game_line_y:
                # Check if ball is hitting the solid parts of the line (not in either hole)
                in_hole1 = (ball.x >= self.hole1_x and ball.x <= self.hole1_x + self.hole_width)
                in_hole2 = (ball.x >= self.hole2_x and ball.x <= self.hole2_x + self.hole_width)
                
                if not in_hole1 and not in_hole2:
                    ball.y = self.game_line_y - ball.radius
                    velocity[1] = -velocity[1] * self.bounce_damping
            
            # Update ball rotation
            ball.update(dt)
        
        # Remove balls that fell through the hole (in reverse order to maintain indices)
        for i in reversed(balls_to_remove):
            self.balls.pop(i)
            self.ball_velocities.pop(i)
        
        # Check for game over
        if len(self.balls) == 0 and not self.game_over:
            self.game_over = True
            self.game_over_start_time = pygame.time.get_ticks()
        
        # Check if game over duration has passed
        if self.game_over and pygame.time.get_ticks() - self.game_over_start_time > self.game_over_duration:
            self.asking_restart = True
        
        # Check ball-to-ball collisions
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                self.check_ball_collision(
                    self.balls[i], self.ball_velocities[i],
                    self.balls[j], self.ball_velocities[j]
                )
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.game_over = False
        self.asking_restart = False
        self.game_over_start_time = 0
        self.score = 0  # Reset score for new game
        
        # Clear existing balls and velocities
        self.balls.clear()
        self.ball_velocities.clear()
        
        # Reinitialize balls
        self.initialize_balls()
        
        # Reset bumpers to initial position
        for bumper in self.bumpers:
            bumper.x = (self.width - bumper.width) // 2
            bumper.y = self.game_line_y - bumper.height - 20
    
    def draw_grid(self):
        grid_size = 50
        for x in range(0, self.width, grid_size):
            pygame.draw.line(self.screen, self.grid_color, (x, 0), (x, self.height))
        for y in range(0, self.height, grid_size):
            pygame.draw.line(self.screen, self.grid_color, (0, y), (self.width, y))
    
    def draw_game_line(self):
        """Draw the game line with two holes in the middle"""
        # Draw left segment of the line (before first hole)
        pygame.draw.line(self.screen, self.line_color, (0, self.game_line_y), 
                        (self.hole1_x, self.game_line_y), 3)
        # Draw middle segment of the line (between holes)
        pygame.draw.line(self.screen, self.line_color, (self.hole1_x + self.hole_width, self.game_line_y), 
                        (self.hole2_x, self.game_line_y), 3)
        # Draw right segment of the line (after second hole)
        pygame.draw.line(self.screen, self.line_color, (self.hole2_x + self.hole_width, self.game_line_y), 
                        (self.width, self.game_line_y), 3)
    
    def draw_info(self):
        font = pygame.font.Font(None, 24)
        # Show info for first ball and remaining balls count
        if self.balls:
            ball = self.balls[0]
            velocity = self.ball_velocities[0]
            info_text = f"Balls Remaining: {len(self.balls)} | Ball 1: ({int(ball.x)}, {int(ball.y)}) | Speed: ({velocity[0]:.1f}, {velocity[1]:.1f})"
        else:
            info_text = f"Balls Remaining: {len(self.balls)}"
        text_surface = font.render(info_text, True, (100, 100, 100))
        self.screen.blit(text_surface, (10, 10))
        
        # Draw score in top-right corner
        score_text = f"Score: {self.score}"
        score_surface = font.render(score_text, True, (255, 255, 0))  # Yellow color for score
        score_rect = score_surface.get_rect()
        score_rect.topright = (self.width - 10, 10)
        self.screen.blit(score_surface, score_rect)
        
        # Draw flashing GAME OVER message
        if self.game_over and not self.asking_restart:
            game_over_font = pygame.font.Font(None, 72)
            # Flash every 500ms
            if (pygame.time.get_ticks() - self.game_over_start_time) // 500 % 2 == 0:
                game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
                text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2))
                self.screen.blit(game_over_text, text_rect)
        
        # Draw restart prompt
        if self.asking_restart:
            restart_font = pygame.font.Font(None, 48)
            restart_text = restart_font.render("Shall we play again? (y/n)", True, (255, 255, 255))
            text_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(restart_text, text_rect)
        
        controls_text = "SPACE/Click: Activate Bumper | Arrow Keys: Move Bumper | ESC: Quit"
        controls_surface = font.render(controls_text, True, (100, 100, 100))
        self.screen.blit(controls_surface, (10, self.height - 30))
    
    def run(self):
        while self.running:
            dt = self.clock.tick(60)
            self.handle_events()
            
            # Only update physics if game is not over and not asking for restart
            if not self.game_over and not self.asking_restart:
                self.update_physics(dt)
            elif self.game_over and not self.asking_restart:
                # Still update physics for game over detection
                self.update_physics(dt)
            
            self.screen.fill(self.bg_color)
            self.draw_grid()
            
            # Draw game line
            self.draw_game_line()
            
            # Draw bumpers
            for bumper in self.bumpers:
                bumper.draw(self.screen)
            
            # Draw all balls
            for ball in self.balls:
                ball.draw(self.screen)
            
            self.draw_info()
            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    app = BouncyBallApp()
    app.run() 