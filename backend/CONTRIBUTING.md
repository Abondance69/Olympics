# 🤝 Guide de Contribution

Merci de votre intérêt pour contribuer au projet Olympics Analytics !

## 📋 Prérequis

- Node.js v16+
- npm ou yarn
- Git
- Base de données (MySQL/MariaDB ou PostgreSQL)
- Connaissances en React, TypeScript, Express.js

---

## 🚀 Premiers pas

### 1. Fork et Clone

```bash
# Fork le projet sur GitHub
# Puis cloner votre fork
git clone https://github.com/VOTRE-USERNAME/hackathon-olympics.git
cd hackathon-olympics
```

### 2. Installation

```powershell
# Utiliser le script d'installation
.\scripts\install.ps1

# OU manuellement
cd backend && npm install
cd ..\frontend && npm install
```

### 3. Configuration

Copier les fichiers `.env.example` vers `.env` et configurer vos variables.

### 4. Créer une branche

```bash
git checkout -b feature/ma-nouvelle-fonctionnalite
# ou
git checkout -b fix/correction-bug
```

---

## 📝 Standards de Code

### Backend (Node.js/Express)

```javascript
// ✅ BON
const express = require('express');
const router = express.Router();

router.get('/endpoint', async (req, res) => {
  try {
    // Logique
    res.json(data);
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Message d\'erreur' });
  }
});

// ❌ MAUVAIS
router.get('/endpoint', (req, res) => {
  // Pas de gestion d'erreur
  res.json(data);
});
```

### Frontend (React/TypeScript)

```typescript
// ✅ BON
import React, { useState, useEffect } from 'react';

interface Props {
  title: string;
  onSubmit: (data: string) => void;
}

const MyComponent: React.FC<Props> = ({ title, onSubmit }) => {
  const [data, setData] = useState<string>('');
  
  useEffect(() => {
    // Effet
  }, []);

  return (
    <div className="my-component">
      <h2>{title}</h2>
    </div>
  );
};

export default MyComponent;

// ❌ MAUVAIS
const MyComponent = (props) => {
  // Pas de typage
  return <div>{props.title}</div>;
};
```

### CSS

```css
/* ✅ BON - Utiliser les variables CSS */
.my-component {
  color: var(--primary-color);
  padding: var(--spacing-md);
  border-radius: var(--border-radius);
}

/* ❌ MAUVAIS - Valeurs en dur */
.my-component {
  color: #0066cc;
  padding: 16px;
  border-radius: 8px;
}
```

---

## 🧪 Tests

### Backend

```javascript
// Ajouter des tests avec Jest (à venir)
describe('Stats API', () => {
  it('should return overview stats', async () => {
    // Test
  });
});
```

### Frontend

```typescript
// Tester les composants avec React Testing Library
import { render, screen } from '@testing-library/react';
import MyComponent from './MyComponent';

test('renders component', () => {
  render(<MyComponent title="Test" />);
  expect(screen.getByText('Test')).toBeInTheDocument();
});
```

---

## 🎨 Convention de nommage

### Fichiers

- **Composants React** : `PascalCase.tsx` (ex: `Header.tsx`)
- **Hooks custom** : `camelCase.ts` (ex: `useApi.ts`)
- **Utilitaires** : `camelCase.ts` (ex: `formatDate.ts`)
- **CSS** : Même nom que le composant (ex: `Header.css`)

### Variables

```typescript
// ✅ BON
const userName = 'John';
const API_BASE_URL = 'http://localhost:5000';
const MAX_RETRIES = 3;

interface UserData {
  firstName: string;
  lastName: string;
}

// ❌ MAUVAIS
const user_name = 'John';
const apibaseurl = 'http://localhost:5000';
```

---

## 📁 Structure des commits

### Format

```
type(scope): sujet

corps (optionnel)

footer (optionnel)
```

### Types

- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation
- `style`: Formatage, CSS
- `refactor`: Refactorisation
- `test`: Ajout de tests
- `chore`: Maintenance

### Exemples

```bash
feat(predictions): ajouter graphique clustering
fix(api): corriger erreur CORS
docs(readme): mettre à jour instructions installation
style(header): améliorer responsive mobile
refactor(api): simplifier routes medals
```

---

## 🔄 Workflow de contribution

### 1. Développer

```bash
# Créer une branche
git checkout -b feature/ma-feature

# Développer et tester
npm run dev

# Commit réguliers
git add .
git commit -m "feat(scope): description"
```

### 2. Pull Request

```bash
# Push vers votre fork
git push origin feature/ma-feature

# Créer une PR sur GitHub
# Titre clair et description détaillée
```

### 3. Code Review

- Attendre la review
- Répondre aux commentaires
- Corriger si nécessaire
- Une fois approuvé, merge par un mainteneur

---

## 🐛 Rapporter un bug

### Template

```markdown
**Description du bug**
Description claire et concise.

**Pour reproduire**
1. Aller sur '...'
2. Cliquer sur '...'
3. Voir l'erreur

**Comportement attendu**
Ce qui devrait se passer.

**Screenshots**
Si applicable.

**Environnement**
- OS: [ex: Windows 11]
- Navigateur: [ex: Chrome 120]
- Version Node: [ex: 18.0.0]

**Informations additionnelles**
Tout autre contexte.
```

---

## ✨ Proposer une fonctionnalité

### Template

```markdown
**Problème résolu**
Quel problème cette feature résout-elle ?

**Solution proposée**
Comment voulez-vous résoudre ce problème ?

**Alternatives**
Avez-vous considéré d'autres solutions ?

**Contexte additionnel**
Screenshots, maquettes, exemples.
```

---

## 📚 Ressources pour contribuer

### Documentation

- [React Docs](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Express.js Guide](https://expressjs.com/en/guide/routing.html)
- [Plotly.js Docs](https://plotly.com/javascript/)

### Outils utiles

- [VS Code](https://code.visualstudio.com/)
- [Postman](https://www.postman.com/) - Test API
- [React DevTools](https://react.dev/learn/react-developer-tools)
- [Git](https://git-scm.com/)

### Extensions VS Code recommandées

- ESLint
- Prettier
- TypeScript Vue Plugin
- Auto Rename Tag
- GitLens

---

## ✅ Checklist avant PR

- [ ] Le code compile sans erreur
- [ ] Le code suit les standards du projet
- [ ] Les tests passent (si applicable)
- [ ] La documentation est à jour
- [ ] Les commits sont bien formatés
- [ ] Pas de `console.log` inutiles
- [ ] Pas de fichiers `.env` commitées
- [ ] Le responsive est testé
- [ ] Les performances sont bonnes

---

## 🎓 Bonnes pratiques

### Performance

```typescript
// ✅ Utiliser useMemo pour calculs coûteux
const expensiveValue = useMemo(() => {
  return computeExpensiveValue(data);
}, [data]);

// ✅ Utiliser useCallback pour fonctions
const handleClick = useCallback(() => {
  // Action
}, [dependencies]);
```

### Accessibilité

```tsx
// ✅ BON
<button aria-label="Fermer" onClick={onClose}>
  ×
</button>

<img src="logo.png" alt="Logo Olympics" />

// ❌ MAUVAIS
<div onClick={onClose}>×</div>
<img src="logo.png" />
```

### Sécurité

```javascript
// ✅ Validation des entrées
const sanitizeInput = (input) => {
  return input.trim().replace(/[<>]/g, '');
};

// ✅ Utiliser des variables d'environnement
const apiKey = process.env.API_KEY;
```

---

## 💬 Communication

- **Questions** : Ouvrir une issue
- **Discussions** : GitHub Discussions
- **Bugs** : Issue avec le label `bug`
- **Features** : Issue avec le label `enhancement`

---

## 📜 Licence

En contribuant, vous acceptez que vos contributions soient sous la même licence que le projet.

---

## 🙏 Remerciements

Merci à tous les contributeurs qui rendent ce projet meilleur ! 🎉

---

**Questions ?** N'hésitez pas à ouvrir une issue ou à contacter l'équipe !
