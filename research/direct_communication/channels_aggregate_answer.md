# Do Many Channels Add Up, or Are You Stuck With One Channel's Worth?

**YES, they add up.** Total data capacity is the SUM of all the separate frequency channels you hold (each channel carries about its bandwidth times an efficiency, and modern phones combine multiple channels at once so their rates add), so holding many channels gives many channels' worth, not one; the only limit is how much spectrum you have acquired, which is a licensing and business limit, not a per-channel physics cap.

## The plain-language explanation

One channel of width B (say 25 MHz) carries roughly B times a "spectral efficiency" number set by signal quality. That is the Shannon-Hartley law: capacity = bandwidth times log2(1 + signal-to-noise). So a single channel does have a ceiling, but that ceiling is per channel, not per system. (See `spectrum_capacity_primer.md`, Section 2, COMM-427/428.)

The key fact is that a phone is not stuck on one channel. Since 2011, the cellular standard (3GPP, in the LTE-Advanced release called Release 10) has a feature named CARRIER AGGREGATION: one device receives and transmits on several separate frequency blocks (called "component carriers") at the same time, and the throughputs ADD UP to the combined bandwidth. LTE-Advanced aggregates up to 5 carriers for up to 100 MHz total, and that is exactly how carriers reached "Gigabit LTE." 5G NR widens it further (the standard allows up to 16 carriers, and operators advertise roughly 4 Gbps and up by combining bands). So if you hold three 25 MHz channels and a device aggregates them, it sees 75 MHz worth, not 25. Total capacity = (sum of all the channel bandwidths you hold) times efficiency. More channels held means more total capacity, summed. The bound is simply how much spectrum you have acquired. (See `spectrum_capacity_primer.md`, Section 4, COMM-433.)

One distinction matters so you are not misled. Splitting ONE channel into many tiny "subcarriers" (the OFDMA method inside LTE and 5G) does NOT add capacity. Subcarriers are a multiple-access trick: they let many users politely share that one channel, but the total stays one channel's worth (bandwidth times efficiency), no matter how finely you slice it. That is the case people confuse with aggregation. The rule of thumb: subcarriers WITHIN one channel divide a fixed pie among users; SEPARATE channels at different frequencies are different pies that add together. Your intuition that "the many channels around that frequency sum" is the aggregation case, and it is correct. (See `spectrum_capacity_primer.md`, Section 5, COMM-434.)

## Citations (open these yourself, line by line)

1. Carrier aggregation, the standard itself. "Carrier aggregation was introduced in 3GPP Release 10 (LTE-Advanced) to provide wider than 20 MHz transmission bandwidth to a single device" and "two or more component carriers can be aggregated to support wider transmission bandwidths up to 100 MHz." 3GPP LTE-Advanced overview (authored for 3GPP): https://www.3gpp.org/img/pdf/lte_advanced_v2.pdf and the 3GPP technology page: https://www.3gpp.org/technologies/carrier-aggregation-on-mobile-networks

2. Carrier aggregation, plain reference with the numbers. "Multiple frequency blocks (called component carriers) are assigned to the same user," and "since LTE Release 10 up to 5 component carriers may be aggregated, allowing for transmission bandwidths of up to 100 MHz." Wikipedia, Carrier aggregation: https://en.wikipedia.org/wiki/Carrier_aggregation

3. Shannon-Hartley law (the per-channel ceiling). "C = B log2(1 + S/N)," where C is "the channel capacity in bits per second," B is "the bandwidth of the channel in hertz," and S/N is "the signal-to-noise ratio ... expressed as a linear power ratio." Wikipedia, Shannon-Hartley theorem: https://en.wikipedia.org/wiki/Shannon%E2%80%93Hartley_theorem

4. 5G carrier aggregation, operator source. Carrier aggregation lets operators "combine the capabilities of radio cells at distinct frequency allocations," and in 5G it enables "user data rates of about 4 Gbps and above"; Nokia demonstrated four-carrier 5G aggregation at MWC 2022. Nokia, 5G Carrier Aggregation explained: https://www.nokia.com/mobile-networks/ran/carrier-aggregation/5g-carrier-aggregation-explained/

5. The distinction: OFDMA subcarriers are multiple access (sharing one channel), not added capacity. OFDMA is "a multi-user variant of OFDM ... it allows for multiple access" by "assigning subsets of time-frequency resource units to multiple users." TechTarget, OFDMA definition: https://www.techtarget.com/searchnetworking/definition/orthogonal-frequency-division-multiple-access-OFDMA

6. In-house grounding (the same conclusions, with the satellite direct-to-cell context and full source list): `research/direct_communication/spectrum_capacity_primer.md`, Sections 2, 4, and 5 (claims COMM-427, COMM-428, COMM-433, COMM-434).
