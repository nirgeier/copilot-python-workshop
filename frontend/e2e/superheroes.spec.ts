import { test, expect } from '@playwright/test';

test.describe('Superhero Application', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display the header', async ({ page }) => {
    await expect(page.getByText('Superhero Management')).toBeVisible();
  });

  test('should display list of superheroes', async ({ page }) => {
    // Wait for the table to be visible
    const table = page.locator('table');
    await expect(table).toBeVisible();

    // Check for table headers
    const headers = ['ID', 'Image', 'Name', 'Intelligence', 'Strength', 'Speed', 'Durability', 'Power', 'Combat'];
    for (const header of headers) {
      await expect(page.getByRole('columnheader', { name: header })).toBeVisible();
    }

    // Verify some superhero data is loaded
    await expect(page.getByRole('row')).toHaveCount.above(1); // At least header row + 1 data row
  });

  test('should allow selecting heroes for comparison', async ({ page }) => {
    // Select first two heroes
    const rows = page.locator('tbody tr');
    await rows.nth(0).click();
    await rows.nth(1).click();

    // Verify they are selected
    await expect(rows.nth(0)).toHaveClass(/selected/);
    await expect(rows.nth(1)).toHaveClass(/selected/);

    // Verify compare button is enabled
    const compareButton = page.getByRole('button', { name: 'Compare Selected Heroes' });
    await expect(compareButton).toBeEnabled();
  });

  test('should navigate to comparison page', async ({ page }) => {
    // Select two heroes and navigate to comparison
    const rows = page.locator('tbody tr');
    await rows.nth(0).click();
    await rows.nth(1).click();
    await page.getByRole('button', { name: 'Compare Selected Heroes' }).click();

    // Verify we're on the comparison page
    await expect(page.getByText('Superhero Comparison')).toBeVisible();
    
    // Verify comparison data is shown
    await expect(page.locator('.comparison-grid')).toBeVisible();
    await expect(page.locator('.hero-card')).toHaveCount(2);
    await expect(page.locator('.stats-comparison')).toBeVisible();
  });

  test('should handle error states gracefully', async ({ page, context }) => {
    // Mock failed API response
    await context.route('**/superheroes/all', async route => {
      await route.fulfill({
        status: 500,
        body: JSON.stringify({ error: 'Internal Server Error' })
      });
    });

    // Refresh page to trigger error state
    await page.reload();

    // Verify error handling (assuming error message is shown)
    await expect(page.locator('table')).not.toBeVisible();
  });

  test('should allow deselecting heroes', async ({ page }) => {
    const rows = page.locator('tbody tr');
    
    // Select a hero
    await rows.nth(0).click();
    await expect(rows.nth(0)).toHaveClass(/selected/);
    
    // Deselect the hero
    await rows.nth(0).click();
    await expect(rows.nth(0)).not.toHaveClass(/selected/);
  });

  test('should limit hero selection to two', async ({ page }) => {
    const rows = page.locator('tbody tr');
    
    // Select three heroes
    await rows.nth(0).click();
    await rows.nth(1).click();
    await rows.nth(2).click();
    
    // Verify only two are selected
    const selectedRows = page.locator('tbody tr.selected');
    await expect(selectedRows).toHaveCount(2);
  });
});