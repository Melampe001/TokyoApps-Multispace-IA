#!/usr/bin/env python3
"""
SYNEMU Agent 2D Flare
=====================

Specialized agent for 2D simulation, sprite animation, and 2D physics emulation
using the Flare engine framework.

Part of: Tokyo-IA SYNEMU Suite (TokyoApps® / TokRaggcorp®)
Agent ID: synemu-2d-flare-002
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from .synemu_integrations import get_integrations

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Sprite2D:
    """Represents a 2D sprite in the simulation"""
    sprite_id: str
    position: Tuple[float, float]
    size: Tuple[float, float]
    texture: Optional[str] = None
    velocity: Tuple[float, float] = (0.0, 0.0)
    rotation: float = 0.0
    scale: float = 1.0


@dataclass
class SimulationScene2D:
    """Represents a 2D simulation scene"""
    scene_id: str
    width: int
    height: int
    sprites: List[Sprite2D]
    background_color: str = "#000000"
    gravity: Tuple[float, float] = (0.0, -9.8)
    timestep: float = 0.016  # ~60 FPS


class Synemu2DFlareAgent:
    """
    SYNEMU 2D Flare Agent
    
    Handles 2D simulation and emulation tasks including:
    - Sprite-based animations
    - 2D physics simulations
    - Particle systems
    - 2D scene management
    - Collision detection
    - State transitions
    
    Attributes:
        agent_id: Unique identifier
        name: Human-readable name
        version: Agent version
    """
    
    AGENT_ID = "synemu-2d-flare-002"
    NAME = "SYNEMU 2D Flare"
    VERSION = "1.0.0"
    EMOJI = "🔥"
    
    def __init__(self):
        """Initialize the 2D Flare agent"""
        self.integrations = get_integrations()
        self.config = self.integrations.get_simulation_config("2d")
        self.active_scenes: Dict[str, SimulationScene2D] = {}
        self.simulation_history: List[Dict[str, Any]] = []
        
        logger.info(f"{self.EMOJI} {self.NAME} v{self.VERSION} initialized")
    
    def create_scene(
        self,
        width: int = 1920,
        height: int = 1080,
        background_color: str = "#000000"
    ) -> str:
        """
        Create a new 2D simulation scene.
        
        Args:
            width: Scene width in pixels
            height: Scene height in pixels
            background_color: Background color in hex format
            
        Returns:
            Scene ID string
        """
        scene_id = f"scene2d-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        scene = SimulationScene2D(
            scene_id=scene_id,
            width=width,
            height=height,
            sprites=[],
            background_color=background_color,
        )
        
        self.active_scenes[scene_id] = scene
        logger.info(f"Created 2D scene: {scene_id} ({width}x{height})")
        
        return scene_id
    
    def add_sprite(
        self,
        scene_id: str,
        position: Tuple[float, float],
        size: Tuple[float, float],
        texture: Optional[str] = None
    ) -> str:
        """
        Add a sprite to a scene.
        
        Args:
            scene_id: Target scene identifier
            position: (x, y) position in scene coordinates
            size: (width, height) of the sprite
            texture: Optional texture path or identifier
            
        Returns:
            Sprite ID string
        """
        if scene_id not in self.active_scenes:
            raise ValueError(f"Scene not found: {scene_id}")
        
        sprite_id = f"sprite-{len(self.active_scenes[scene_id].sprites):04d}"
        
        sprite = Sprite2D(
            sprite_id=sprite_id,
            position=position,
            size=size,
            texture=texture,
        )
        
        self.active_scenes[scene_id].sprites.append(sprite)
        logger.info(f"Added sprite {sprite_id} to scene {scene_id}")
        
        return sprite_id
    
    def run_simulation(
        self,
        scene_id: str,
        duration: float = 10.0,
        record: bool = False
    ) -> Dict[str, Any]:
        """
        Run a 2D physics simulation.
        
        Args:
            scene_id: Scene to simulate
            duration: Duration in seconds
            record: Whether to record the simulation
            
        Returns:
            Simulation results dictionary
        """
        if scene_id not in self.active_scenes:
            raise ValueError(f"Scene not found: {scene_id}")
        
        scene = self.active_scenes[scene_id]
        timestep = scene.timestep
        num_steps = int(duration / timestep)
        
        logger.info(f"Running simulation for {duration}s ({num_steps} steps)")
        
        # Simulate physics updates
        frames = []
        for step in range(num_steps):
            # Update sprite positions based on velocity and gravity
            for sprite in scene.sprites:
                # Apply gravity
                new_vx = sprite.velocity[0]
                new_vy = sprite.velocity[1] + scene.gravity[1] * timestep
                
                # Update position
                new_x = sprite.position[0] + new_vx * timestep
                new_y = sprite.position[1] + new_vy * timestep
                
                sprite.velocity = (new_vx, new_vy)
                sprite.position = (new_x, new_y)
            
            if record:
                # Record frame state
                frame_state = {
                    "step": step,
                    "time": step * timestep,
                    "sprites": [
                        {
                            "id": s.sprite_id,
                            "position": s.position,
                            "velocity": s.velocity,
                        }
                        for s in scene.sprites
                    ]
                }
                frames.append(frame_state)
        
        result = {
            "scene_id": scene_id,
            "duration": duration,
            "steps": num_steps,
            "sprites": len(scene.sprites),
            "recorded": record,
            "frames": frames if record else [],
        }
        
        self.simulation_history.append({
            "scene_id": scene_id,
            "timestamp": datetime.now().isoformat(),
            "result": result,
        })
        
        logger.info(f"Simulation completed: {num_steps} steps")
        return result
    
    def detect_collisions(self, scene_id: str) -> List[Dict[str, Any]]:
        """
        Detect collisions between sprites in a scene.
        
        Args:
            scene_id: Scene to check
            
        Returns:
            List of collision events
        """
        if scene_id not in self.active_scenes:
            raise ValueError(f"Scene not found: {scene_id}")
        
        scene = self.active_scenes[scene_id]
        collisions = []
        
        # Simple AABB collision detection
        for i, sprite_a in enumerate(scene.sprites):
            for sprite_b in scene.sprites[i + 1:]:
                if self._check_aabb_collision(sprite_a, sprite_b):
                    collisions.append({
                        "sprite_a": sprite_a.sprite_id,
                        "sprite_b": sprite_b.sprite_id,
                        "position_a": sprite_a.position,
                        "position_b": sprite_b.position,
                    })
        
        logger.info(f"Detected {len(collisions)} collisions in scene {scene_id}")
        return collisions
    
    def _check_aabb_collision(self, sprite_a: Sprite2D, sprite_b: Sprite2D) -> bool:
        """
        Check if two sprites collide using AABB (Axis-Aligned Bounding Box).
        
        Args:
            sprite_a: First sprite
            sprite_b: Second sprite
            
        Returns:
            True if sprites collide, False otherwise
        """
        ax, ay = sprite_a.position
        aw, ah = sprite_a.size
        bx, by = sprite_b.position
        bw, bh = sprite_b.size
        
        return (
            ax < bx + bw and
            ax + aw > bx and
            ay < by + bh and
            ay + ah > by
        )
    
    def export_scene(self, scene_id: str, format: str = "json") -> Dict[str, Any]:
        """
        Export a scene to a specific format.
        
        Args:
            scene_id: Scene to export
            format: Export format (json, yaml, binary)
            
        Returns:
            Exported scene data
        """
        if scene_id not in self.active_scenes:
            raise ValueError(f"Scene not found: {scene_id}")
        
        scene = self.active_scenes[scene_id]
        
        export_data = {
            "scene_id": scene.scene_id,
            "dimensions": {"width": scene.width, "height": scene.height},
            "background_color": scene.background_color,
            "gravity": scene.gravity,
            "timestep": scene.timestep,
            "sprites": [
                {
                    "id": s.sprite_id,
                    "position": s.position,
                    "size": s.size,
                    "texture": s.texture,
                    "velocity": s.velocity,
                    "rotation": s.rotation,
                    "scale": s.scale,
                }
                for s in scene.sprites
            ],
        }
        
        logger.info(f"Exported scene {scene_id} to {format} format")
        return export_data
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get agent status and statistics.
        
        Returns:
            Status dictionary
        """
        return {
            "agent_id": self.AGENT_ID,
            "name": self.NAME,
            "version": self.VERSION,
            "active_scenes": len(self.active_scenes),
            "simulations_run": len(self.simulation_history),
            "config": self.config,
        }


def main():
    """Main function for testing and demonstration"""
    print("=" * 70)
    print(f"🔥 SYNEMU 2D Flare Agent v{Synemu2DFlareAgent.VERSION}")
    print("=" * 70)
    print()
    
    agent = Synemu2DFlareAgent()
    
    # Create a test scene
    scene_id = agent.create_scene(width=800, height=600)
    print(f"Created scene: {scene_id}")
    
    # Add some sprites
    agent.add_sprite(scene_id, position=(100, 500), size=(50, 50), texture="ball.png")
    agent.add_sprite(scene_id, position=(200, 400), size=(50, 50), texture="box.png")
    
    # Run simulation
    result = agent.run_simulation(scene_id, duration=5.0, record=False)
    print(f"\nSimulation completed:")
    print(f"  Duration: {result['duration']}s")
    print(f"  Steps: {result['steps']}")
    print(f"  Sprites: {result['sprites']}")
    
    # Check status
    status = agent.get_status()
    print(f"\nAgent Status:")
    print(f"  Active scenes: {status['active_scenes']}")
    print(f"  Simulations run: {status['simulations_run']}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
