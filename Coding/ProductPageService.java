public Mono<ProductPage> productPage(String sku) {
    Mono<Product> productMono = catalog.getProduct(sku)
            .timeout(Duration.ofSeconds(2));

    Mono<Stock> stockMono = inventory.getStock(sku)
            .timeout(Duration.ofSeconds(2))
            .onErrorReturn(Stock.unknown(sku));

    Mono<List<Review>> reviewsMono = reviews.getReviews(sku)
            .timeout(Duration.ofSeconds(2))
            .collectList()
            .onErrorReturn(List.of());

    return Mono.zip(productMono, stockMono, reviewsMono)
            .map(result -> new ProductPage(
                    result.getT1(),
                    result.getT2(),
                    result.getT3()
            ));
}
