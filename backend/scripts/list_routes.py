"""Print registered FastAPI routes for debugging."""
from app.main import app

def list_routes():
    routes = set()
    for r in app.routes:
        if hasattr(r, 'methods'):
            for m in r.methods:
                if m in ('HEAD', 'OPTIONS'):
                    continue
                routes.add((m, r.path))
    for m, p in sorted(routes):
        print(m, p)

if __name__ == '__main__':
    list_routes()
