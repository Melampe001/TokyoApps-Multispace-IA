/**
 * Context management for MCP server
 * Handles conversation context and state management
 */

class ContextManager {
  constructor() {
    this.contexts = new Map();
  }

  /**
   * Create or update context
   */
  setContext(contextId, data) {
    this.contexts.set(contextId, {
      ...data,
      updatedAt: new Date().toISOString()
    });
  }

  /**
   * Retrieve context
   */
  getContext(contextId) {
    return this.contexts.get(contextId) || null;
  }

  /**
   * Delete context
   */
  deleteContext(contextId) {
    return this.contexts.delete(contextId);
  }

  /**
   * List all contexts
   */
  listContexts() {
    return Array.from(this.contexts.entries()).map(([id, data]) => ({
      id,
      ...data
    }));
  }

  /**
   * Clear expired contexts (older than 24 hours)
   */
  cleanupExpired() {
    const now = new Date();
    const dayAgo = new Date(now.getTime() - 24 * 60 * 60 * 1000);
    
    for (const [id, data] of this.contexts.entries()) {
      if (new Date(data.updatedAt) < dayAgo) {
        this.contexts.delete(id);
      }
    }
  }
}

export default new ContextManager();
