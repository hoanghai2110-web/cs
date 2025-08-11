<?php
require_once 'countries.php';
require_once 'partials/header.php';
?>

<div class="min-h-screen bg-gray-50">
    <!-- Warning Banner -->
    <div class="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4">
        <div class="flex">
            <div class="flex-shrink-0">
                <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
            </div>
            <div class="ml-3">
                <p class="text-sm">
                    <strong>Demo Only</strong> — No real phone numbers. This is a sandbox for demonstration purposes only.
                </p>
            </div>
        </div>
    </div>

    <div class="container mx-auto px-4 py-8">
        <div class="text-center mb-8">
            <h1 class="text-4xl font-bold text-gray-900 mb-4">SMS Receiver Sandbox</h1>
            <p class="text-lg text-gray-600">Select a country to view virtual phone numbers and receive demo SMS messages</p>
        </div>

        <!-- Countries Grid -->
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
            <?php foreach ($countries as $country): ?>
                <a href="country.php?cc=<?= urlencode($country['cc']) ?>" 
                   class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 p-4 block hover:bg-gray-50">
                    <div class="text-center">
                        <div class="text-2xl mb-2"><?= $country['flag'] ?></div>
                        <div class="text-sm font-medium text-gray-900 mb-1"><?= htmlspecialchars($country['name']) ?></div>
                        <div class="text-xs text-gray-500"><?= htmlspecialchars($country['cc']) ?></div>
                    </div>
                </a>
            <?php endforeach; ?>
        </div>

        <div class="mt-12 text-center">
            <div class="bg-blue-50 rounded-lg p-6">
                <h2 class="text-lg font-semibold text-blue-900 mb-2">How it works</h2>
                <p class="text-blue-700 text-sm">
                    1. Choose a country → 2. Select a virtual number → 3. View demo SMS messages
                </p>
                <p class="text-blue-600 text-xs mt-2">
                    All phone numbers and messages are generated for demonstration purposes only
                </p>
            </div>
        </div>
    </div>
</div>

<?php require_once 'partials/footer.php'; ?>
