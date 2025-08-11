    <!-- Footer -->
    <footer class="bg-gray-800 text-white mt-12">
        <div class="container mx-auto px-4 py-8">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div>
                    <h3 class="text-lg font-semibold mb-4">SMS Receiver Sandbox</h3>
                    <p class="text-gray-300 text-sm">
                        A demonstration platform for virtual SMS reception. All phone numbers and messages are generated for testing purposes only.
                    </p>
                </div>
                
                <div>
                    <h4 class="text-md font-semibold mb-4">Important Notice</h4>
                    <ul class="text-gray-300 text-sm space-y-2">
                        <li>• No real phone numbers</li>
                        <li>• All messages are fake/generated</li>
                        <li>• For demonstration only</li>
                        <li>• Numbers change daily</li>
                    </ul>
                </div>
                
                <div>
                    <h4 class="text-md font-semibold mb-4">Quick Links</h4>
                    <ul class="text-gray-300 text-sm space-y-2">
                        <li><a href="index.php" class="hover:text-white">All Countries</a></li>
                        <li><a href="sitemap.php" class="hover:text-white">Sitemap</a></li>
                    </ul>
                </div>
            </div>
            
            <div class="border-t border-gray-700 mt-8 pt-6">
                <div class="flex flex-col md:flex-row justify-between items-center">
                    <div class="text-gray-400 text-sm">
                        <strong>Sandbox Demo</strong> — Messages are generated and not real. This platform is for demonstration purposes only.
                    </div>
                    <div class="text-gray-500 text-xs mt-2 md:mt-0">
                        © <?= date('Y') ?> SMS Receiver Sandbox. Demo Environment.
                    </div>
                </div>
            </div>
        </div>
    </footer>
</body>
</html>
