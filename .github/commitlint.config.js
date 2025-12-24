// Configuración de commitlint para validar mensajes de commit
// Sigue la especificación de Conventional Commits
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',     // Nueva funcionalidad
        'fix',      // Corrección de bugs
        'docs',     // Cambios en documentación
        'style',    // Cambios de formato (espacios, comas, etc)
        'refactor', // Refactorización de código
        'perf',     // Mejoras de rendimiento
        'test',     // Añadir o corregir tests
        'build',    // Cambios en el sistema de build
        'ci',       // Cambios en CI/CD
        'chore',    // Tareas de mantenimiento
        'revert',   // Revertir cambios previos
      ],
    ],
    'subject-case': [0],
    'subject-empty': [2, 'never'],
    'subject-full-stop': [2, 'never', '.'],
    'header-max-length': [2, 'always', 100],
  },
};
