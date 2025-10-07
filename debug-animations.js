// Animation Debugging Script
// Run this in the browser console to diagnose multiple animations

console.clear();
console.log('=== ANIMATION DEBUG REPORT ===\n');

// 1. Count all canvas elements
const allCanvases = document.querySelectorAll('canvas');
console.log(`Total canvas elements: ${allCanvases.length}`);

// 2. Check which canvases are visible in viewport
const visibleCanvases = Array.from(allCanvases).filter(c => {
  const rect = c.getBoundingClientRect();
  const viewHeight = window.innerHeight;
  const viewWidth = window.innerWidth;
  return (
    rect.bottom > 0 &&
    rect.right > 0 &&
    rect.top < viewHeight &&
    rect.left < viewWidth
  );
});

console.log(`\nVisible canvases in viewport: ${visibleCanvases.length}`);
visibleCanvases.forEach((canvas, i) => {
  const rect = canvas.getBoundingClientRect();
  console.log(`  [${i}] ${canvas.className}`);
  console.log(`      Position: top=${rect.top.toFixed(0)}px, left=${rect.left.toFixed(0)}px`);
  console.log(`      Size: ${rect.width.toFixed(0)}x${rect.height.toFixed(0)}px`);
  console.log(`      Z-index: ${window.getComputedStyle(canvas).zIndex}`);
  console.log(`      Opacity: ${window.getComputedStyle(canvas).opacity}`);
});

// 3. Check which slides are currently mounted
const slides = document.querySelectorAll('.slidev-page');
console.log(`\nTotal mounted slides: ${slides.length}`);

const activeSlide = Array.from(slides).find(s =>
  window.getComputedStyle(s).display !== 'none' &&
  parseFloat(window.getComputedStyle(s).opacity) > 0.5
);

if (activeSlide) {
  const slideNum = activeSlide.className.match(/slidev-page-(\d+)/)?.[1];
  console.log(`Active slide: ${slideNum}`);

  // Find canvases within this slide
  const slideCanvases = activeSlide.querySelectorAll('canvas');
  console.log(`  Canvases in active slide: ${slideCanvases.length}`);
  slideCanvases.forEach((canvas, i) => {
    console.log(`    [${i}] ${canvas.className}`);
  });
}

// 4. Check for multiple WebGL contexts
console.log('\n=== WebGL Context Check ===');
const originalGetContext = HTMLCanvasElement.prototype.getContext;
let glContextCount = 0;
HTMLCanvasElement.prototype.getContext = function(...args) {
  const result = originalGetContext.apply(this, args);
  if (args[0] === 'webgl' || args[0] === 'webgl2') {
    glContextCount++;
  }
  return result;
};

console.log(`Active WebGL contexts: Checking...`);

// 5. Monitor requestAnimationFrame calls
let rafCallCount = 0;
const rafStart = Date.now();
const originalRAF = window.requestAnimationFrame;
window.requestAnimationFrame = function(callback) {
  rafCallCount++;
  return originalRAF.call(window, callback);
};

setTimeout(() => {
  const elapsed = (Date.now() - rafStart) / 1000;
  const fps = (rafCallCount / elapsed).toFixed(1);
  console.log(`\n=== Animation Loop Stats (${elapsed.toFixed(1)}s sample) ===`);
  console.log(`requestAnimationFrame calls: ${rafCallCount}`);
  console.log(`Estimated FPS: ${fps}`);
  console.log(`Expected calls for 1 animation: ~${(elapsed * 60).toFixed(0)}`);
  console.log(`Expected calls for 2 animations: ~${(elapsed * 120).toFixed(0)}`);

  if (rafCallCount > elapsed * 90) {
    console.warn('⚠️  Multiple animation loops detected!');
  } else {
    console.log('✓ Single animation loop confirmed');
  }
}, 2000);

// 6. Check old slides.md vs slides-new.md
console.log('\n=== Current Slidev Entry ===');
console.log(`Page URL: ${window.location.href}`);
console.log(`Page title: ${document.title}`);

// 7. Check for SlideLayout components
const slideLayouts = document.querySelectorAll('[class*="slide-container"]');
console.log(`\nSlideLayout containers found: ${slideLayouts.length}`);

console.log('\n=== END DEBUG REPORT ===');
console.log('Waiting 2 seconds for RAF stats...\n');
