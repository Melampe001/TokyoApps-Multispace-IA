// Package main provides the main entry point for Tokyo-IA.
// Este archivo es el punto de entrada principal para el sistema Tokyo-IA.
// Se puede extender para inicializar módulos de IA, servicios web, etc.
package main

import (
	"fmt"

	"github.com/Melampe001/Tokyo-IA/internal/ai"
)

// Run es el punto de entrada de la aplicación Tokyo-IA.
// Inicia la aplicación y muestra un mensaje de bienvenida.
// Esta función puede ser llamada desde main() para iniciar el sistema.
func Run() {
	fmt.Println("=== Tokyo-IA ===")
	fmt.Println("Iniciando sistema de IA...")

	// Ejemplo de uso del módulo de IA
	greeting := ai.Greet("Usuario")
	fmt.Println(greeting)

	fmt.Println("Tokyo-IA listo para colaboración.")
}
