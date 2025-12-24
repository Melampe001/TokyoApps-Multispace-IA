// Package ai provides AI-related functionality for Tokyo-IA.
// Este paquete contiene la lógica central de IA del sistema.
// Se puede extender para incluir modelos de ML, procesamiento de lenguaje natural, etc.
package ai

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

// Greet devuelve un mensaje de saludo personalizado.
// Esta función sirve como ejemplo básico de interacción con el módulo de IA.
func Greet(name string) string {
	return fmt.Sprintf("¡Hola, %s! Bienvenido a Tokyo-IA.", name)
}

// Process es un placeholder para el procesamiento de entradas de IA.
// Esta función puede ser extendida para implementar lógica de inferencia.
func Process(input string) string {
	if input == "" {
		return "No se recibió entrada para procesar."
	}
	return fmt.Sprintf("Procesando entrada: %s", input)
}

// Version devuelve la versión actual del módulo de IA desde el archivo VERSION.
func Version() string {
	// Intenta leer desde el archivo VERSION en la raíz del proyecto
	versionFile := filepath.Join("..", "..", "VERSION")
	if data, err := os.ReadFile(versionFile); err == nil {
		return strings.TrimSpace(string(data))
	}
	// Fallback si no se encuentra el archivo
	return "0.1.0"
}
