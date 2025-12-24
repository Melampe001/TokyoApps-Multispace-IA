// Package ai provides AI-related functionality for Tokyo-IA.
// Este paquete contiene la lógica central de IA del sistema.
// Se puede extender para incluir modelos de ML, procesamiento de lenguaje natural, etc.
package ai

import (
	"fmt"
	"os"
	"path/filepath"
	"runtime"
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
	// Intenta determinar la ruta al archivo VERSION usando diferentes métodos
	var versionPaths []string

	// Método 1: Relativo al archivo actual (usando runtime.Caller)
	_, filename, _, ok := runtime.Caller(0)
	if ok {
		dir := filepath.Dir(filename)
		versionPaths = append(versionPaths, filepath.Join(dir, "..", "..", "VERSION"))
	}

	// Método 2: Relativo al directorio de trabajo actual
	if wd, err := os.Getwd(); err == nil {
		versionPaths = append(versionPaths, filepath.Join(wd, "VERSION"))
		versionPaths = append(versionPaths, filepath.Join(wd, "..", "..", "VERSION"))
	}

	// Intenta leer de cada ruta posible
	for _, path := range versionPaths {
		if data, err := os.ReadFile(path); err == nil {
			version := strings.TrimSpace(string(data))
			if version != "" {
				return version
			}
		}
	}

	// Fallback si no se encuentra el archivo
	return "0.1.0"
}
