import { mount } from 'svelte';
import Popup from './Popup.svelte';

try {
  const app = mount(Popup, { target: document.body });
  console.log('Popup component initialized:', app);
} catch (error) {
  console.error('Error initializing Popup component:', error);
}