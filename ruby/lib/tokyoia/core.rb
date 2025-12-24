# frozen_string_literal: true

# Tokyo-IA Core Module
# Este módulo proporciona la funcionalidad central de Ruby para Tokyo-IA.
# Se puede extender para incluir lógica de negocio, integraciones, etc.

module TokyoIA
  # Versión del módulo TokyoIA
  VERSION = begin
    version_file = File.expand_path("../../VERSION", __dir__)
    if File.exist?(version_file)
      File.read(version_file).strip.freeze
    else
      "0.1.0"
    end
  end

  # Core proporciona métodos centrales del sistema.
  module Core
    # Saluda a un usuario con un mensaje personalizado.
    # @param name [String] el nombre del usuario
    # @return [String] mensaje de saludo
    def self.greet(name)
      "¡Hola, #{name}! Bienvenido a Tokyo-IA."
    end

    # Procesa una entrada de texto.
    # @param input [String] la entrada a procesar
    # @return [String] resultado del procesamiento
    def self.process(input)
      return "No se recibió entrada para procesar." if input.nil? || input.empty?

      "Procesando entrada: #{input}"
    end

    # Devuelve información sobre el sistema.
    # @return [Hash] información del sistema
    def self.info
      {
        name: "Tokyo-IA",
        version: VERSION,
        language: "Ruby",
        description: "Sistema de IA con temática Tokyo"
      }
    end
  end
end
