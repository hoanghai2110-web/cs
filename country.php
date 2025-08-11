<?php
require_once 'countries.php';
require_once 'partials/header.php';

// Get country code from URL
$cc = isset($_GET['cc']) ? strtoupper($_GET['cc']) : '';

// Find country data
$currentCountry = null;
foreach ($countries as $country) {
    if ($country['cc'] === $cc) {
        $currentCountry = $country;
        break;
    }
}

// Redirect if country not found
if (!$currentCountry) {
    header('Location: index.php');
    exit;
}

// Generate virtual numbers for this country
function generateNumbers($cc, $count = 15) {
    // Seed random generator with country code and current date for consistent daily numbers
    mt_srand(crc32($cc . date('Y-m-d')));
    
    $numbers = [];
    $prefixes = [
        'US' => ['1202', '1303', '1415', '1520', '1617'],
        'GB' => ['4477', '4478', '4479', '4420', '4421'],
        'FR' => ['336', '337', '338', '339'],
        'DE' => ['4915', '4916', '4917', '4930'],
        'IT' => ['393', '334', '335', '336'],
        'ES' => ['346', '647', '648', '649'],
        'CA' => ['1416', '1514', '1604', '1647'],
        'AU' => ['614', '615', '616', '617'],
        'JP' => ['819', '908', '907', '906'],
        'KR' => ['821', '1010', '1011', '1016'],
        'CN' => ['861', '862', '863', '864'],
        'IN' => ['919', '918', '917', '916'],
        'BR' => ['5511', '5521', '5531', '5541'],
        'MX' => ['521', '522', '523', '524'],
        'RU' => ['79', '71', '72', '73'],
    ];
    
    $countryPrefixes = isset($prefixes[$cc]) ? $prefixes[$cc] : ['1555', '1666', '1777'];
    
    for ($i = 0; $i < $count; $i++) {
        $prefix = $countryPrefixes[mt_rand(0, count($countryPrefixes) - 1)];
        $suffix = '';
        
        // Generate remaining digits
        $remainingDigits = 10 - strlen($prefix);
        for ($j = 0; $j < $remainingDigits; $j++) {
            $suffix .= mt_rand(0, 9);
        }
        
        $numbers[] = $prefix . $suffix;
    }
    
    return $numbers;
}

$virtualNumbers = generateNumbers($cc);
?>

<div class="min-h-screen bg-gray-50">
    <!-- Breadcrumb -->
    <div class="bg-white border-b">
        <div class="container mx-auto px-4 py-3">
            <nav class="text-sm">
                <a href="index.php" class="text-blue-600 hover:text-blue-800">← Back to all countries</a>
            </nav>
        </div>
    </div>

    <div class="container mx-auto px-4 py-8">
        <!-- Country Header -->
        <div class="text-center mb-8">
            <div class="text-6xl mb-4"><?= $currentCountry['flag'] ?></div>
            <h1 class="text-3xl font-bold text-gray-900 mb-2"><?= htmlspecialchars($currentCountry['name']) ?></h1>
            <p class="text-gray-600">Virtual phone numbers for <?= htmlspecialchars($currentCountry['name']) ?> (<?= $cc ?>)</p>
        </div>

        <!-- Demo Notice -->
        <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-8">
            <div class="flex items-start">
                <svg class="h-5 w-5 text-yellow-400 mt-0.5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
                </svg>
                <div>
                    <h3 class="text-sm font-medium text-yellow-800">Demo Environment</h3>
                    <p class="text-sm text-yellow-700 mt-1">These are virtual phone numbers that generate fake SMS messages for demonstration purposes. Numbers change daily.</p>
                </div>
            </div>
        </div>

        <!-- Virtual Numbers Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            <?php foreach ($virtualNumbers as $number): ?>
                <a href="inbox.php?cc=<?= urlencode($cc) ?>&n=<?= urlencode($number) ?>" 
                   class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 p-6 block hover:bg-gray-50">
                    <div class="flex items-center justify-between">
                        <div>
                            <div class="text-lg font-mono font-semibold text-gray-900">+<?= htmlspecialchars($number) ?></div>
                            <div class="text-sm text-gray-500 mt-1">Click to view messages</div>
                        </div>
                        <div class="text-green-500">
                            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                            </svg>
                        </div>
                    </div>
                </a>
            <?php endforeach; ?>
        </div>

        <!-- Info Section -->
        <div class="mt-12">
            <div class="bg-blue-50 rounded-lg p-6">
                <h2 class="text-lg font-semibold text-blue-900 mb-3">About Virtual Numbers</h2>
                <div class="text-blue-700 text-sm space-y-2">
                    <p>• Numbers are regenerated daily using deterministic algorithms</p>
                    <p>• Each number receives 8-15 demo SMS messages</p>
                    <p>• Messages include common scenarios: OTP codes, banking alerts, delivery notifications</p>
                    <p>• All content is generated for demonstration purposes only</p>
                </div>
            </div>
        </div>
    </div>
</div>

<?php require_once 'partials/footer.php'; ?>
