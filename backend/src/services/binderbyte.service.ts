import axios from 'axios';
import prisma from '../lib/prisma';
import { regencies, Regency } from '../data/region-data';
import { districts, District } from '../data/district-data';

class BinderByteService {
    /**
     * Search destination locally using region and district data
     */
    async searchDestination(keyword: string) {
        console.log(`Searching destination for: ${keyword}`);

        const lowerKeyword = keyword.toLowerCase();

        // 1. Search in Regencies (Kota/Kabupaten)
        const cityMatches = regencies.filter(r =>
            r.name.toLowerCase().includes(lowerKeyword) ||
            (r.alt_name && r.alt_name.toLowerCase().includes(lowerKeyword))
        ).map(r => ({
            id: r.id,
            name: r.name,
            type: r.name.startsWith('KOTA') ? 'Kota' : 'Kabupaten',
            label: r.name
        }));

        // 2. Search in Districts (Kecamatan)
        const districtMatches = districts.filter(d =>
            d.name.toLowerCase().includes(lowerKeyword)
        ).map(d => {
            // Find parent regency for better label
            const parentRegency = regencies.find(r => r.id === d.regency_id);
            const regencyName = parentRegency ? parentRegency.name : '';

            return {
                id: d.id,
                name: d.name,
                type: 'Kecamatan',
                label: `Kec. ${d.name}, ${regencyName}`
            };
        });

        // Combine and limit
        const allMatches = [...cityMatches, ...districtMatches];
        return allMatches.slice(0, 20);
    }

    /**
     * Calculate Shipping Cost - MANUAL LOGIC
     * Based on zones: Jakarta -> Indonesia regions
     */
    async calculateCost(origin: string, destination: string, weight: number, courier: string) {
        console.log(`Calculating Manual Cost: Origin=${origin} -> Dest=${destination}`);

        try {
            // 1. Find Origin and Destination Details in Local Data
            const originRegency = regencies.find(r => r.id === origin);

            // Destination can be District (7 chars) or Regency (4 chars)
            let destRegencyId = destination;
            let destIsDistrict = false;

            if (destination.length > 4) {
                const district = districts.find(d => d.id === destination);
                if (district) {
                    destRegencyId = district.regency_id;
                    destIsDistrict = true;
                }
            }

            const destRegency = regencies.find(r => r.id === destRegencyId);

            if (!originRegency || !destRegency) {
                console.warn('Manual Calc: Regions not found locally.');
                return this.getManualRates(50000, 55000);
            }

            // 2. Logic Tariff based on Zone
            // Province IDs Reference:
            // 11-21: Sumatra
            // 31-36: Java
            // 51-53: Bali & Nusa Tenggara
            // 61-65: Kalimantan
            // 71-76: Sulawesi
            // 81-82: Maluku
            // 91-94: Papua

            let cost = 30000; // Default
            let etd = '3-5';

            if (originRegency.id === destRegency.id) {
                // SAMA KOTA/KABUPATEN (Jakarta ke Jakarta)
                cost = 12000;
                etd = '1-2';
            } else if (originRegency.province_id === destRegency.province_id) {
                // SAMA PROVINSI (Jakarta Timur ke Jakarta Barat/Bekasi/Depok/Tangerang)
                cost = 16000;
                etd = '1-2';
            } else {
                // BEDA PROVINSI
                const originProvPrefix = originRegency.province_id.substring(0, 1);
                const destProvPrefix = destRegency.province_id.substring(0, 1);

                const originIsJava = ['31', '32', '33', '34', '35', '36'].includes(originRegency.province_id);

                if (originIsJava) {
                    // Logic from Java (Jakarta) to others
                    if (destProvPrefix === '3') {
                        // To Java (Beda Prov)
                        // Bandung: ~20rb, Semarang: ~28rb, Surabaya: ~32rb, Yogya: ~26rb
                        const destProvId = destRegency.province_id;

                        if (destProvId === '32') {
                            // Jawa Barat (Bandung, Bogor area)
                            cost = 20000;
                            etd = '2-3';
                        } else if (destProvId === '33' || destProvId === '34') {
                            // Jawa Tengah & DIY (Semarang, Solo, Yogya)
                            cost = 28000;
                            etd = '3-4';
                        } else if (destProvId === '35') {
                            // Jawa Timur (Surabaya, Malang, Madiun)
                            cost = 32000;
                            etd = '3-5';
                        } else {
                            // Banten
                            cost = 18000;
                            etd = '2-3';
                        }
                    } else if (destProvPrefix === '1' || destProvPrefix === '2') {
                        // To Sumatra
                        // Lampung/Palembang: ~38rb, Medan: ~50rb, Aceh: ~55rb
                        const destProvId = parseInt(destRegency.province_id);

                        if (destProvId >= 11 && destProvId <= 13) {
                            // Sumatra Utara (Aceh, Sumut)
                            cost = 52000;
                            etd = '4-6';
                        } else if (destProvId >= 14 && destProvId <= 15) {
                            // Riau, Kepri
                            cost = 48000;
                            etd = '4-6';
                        } else {
                            // Sumatra Selatan (Jambi, Sumsel, Bengkulu, Lampung, Babel)
                            cost = 40000;
                            etd = '3-5';
                        }
                    } else if (destProvPrefix === '5') {
                        // To Bali/Nusa Tenggara
                        // Bali: ~42rb, Lombok: ~48rb, NTT: ~55rb
                        const destProvId = parseInt(destRegency.province_id);

                        if (destProvId === 51) {
                            // Bali
                            cost = 42000;
                            etd = '3-5';
                        } else if (destProvId === 52) {
                            // NTB (Lombok, Sumbawa)
                            cost = 50000;
                            etd = '4-6';
                        } else {
                            // NTT (Kupang, Flores)
                            cost = 58000;
                            etd = '5-7';
                        }
                    } else if (destProvPrefix === '6') {
                        // To Kalimantan
                        // Pontianak: ~55rb, Balikpapan: ~60rb, Samarinda: ~62rb
                        const destProvId = parseInt(destRegency.province_id);

                        if (destProvId === 61) {
                            // Kalbar (Pontianak)
                            cost = 55000;
                            etd = '4-6';
                        } else if (destProvId === 64 || destProvId === 65) {
                            // Kaltim, Kaltara (Balikpapan, Samarinda)
                            cost = 62000;
                            etd = '4-7';
                        } else {
                            // Kalteng, Kalsel
                            cost = 58000;
                            etd = '4-6';
                        }
                    } else if (destProvPrefix === '7') {
                        // To Sulawesi
                        // Makassar: ~65rb, Manado: ~72rb, Palu: ~70rb
                        const destProvId = parseInt(destRegency.province_id);

                        if (destProvId === 73) {
                            // Sulsel (Makassar)
                            cost = 65000;
                            etd = '4-7';
                        } else if (destProvId === 71) {
                            // Sulut (Manado)
                            cost = 75000;
                            etd = '5-8';
                        } else {
                            // Sulteng, Sulbar, Sultra, Gorontalo
                            cost = 70000;
                            etd = '5-7';
                        }
                    } else if (destProvPrefix === '8') {
                        // To Maluku
                        // Ambon: ~95rb, Ternate: ~100rb
                        cost = 98000;
                        etd = '7-10';
                    } else if (destProvPrefix === '9') {
                        // To Papua
                        // Jayapura: ~125rb, Timika: ~135rb, Sorong: ~130rb
                        cost = 128000;
                        etd = '8-14';
                    } else {
                        // Others / Fallback
                        cost = 50000;
                        etd = '5-7';
                    }
                } else {
                    // Origin NOT Java (General Fallback)
                    if (originProvPrefix === destProvPrefix) {
                        cost = 30000;
                        etd = '3-5';
                    } else {
                        cost = 60000;
                        etd = '5-10';
                    }
                }
            }

            // Adjust by weight (+5000 per kg)
            const weightKg = Math.ceil(weight / 1000);
            if (weightKg > 1) {
                cost += (weightKg - 1) * 5000;
            }

            return this.getManualRates(cost, cost + 5000, etd);

        } catch (error: any) {
            console.error('Manual Cost Error:', error);
            return this.getManualRates(50000, 55000);
        }
    }

    private getManualRates(regularCost: number, expressCost: number, etdReg: string = '2-4') {
        return [
            {
                code: 'wahana',
                name: 'Wahana',
                costs: [
                    {
                        service: 'REG',
                        description: 'Layanan Reguler',
                        cost: [{ value: regularCost, etd: etdReg }]
                    }
                ]
            },
            {
                code: 'lion',
                name: 'Lion Parcel',
                costs: [
                    {
                        service: 'REG',
                        description: 'Layanan Reguler',
                        cost: [{ value: regularCost - 1000, etd: etdReg }]
                    }
                ]
            },
            {
                code: 'sentral',
                name: 'Sentral Cargo',
                costs: [
                    {
                        service: 'REG',
                        description: 'Layanan Reguler',
                        cost: [{ value: regularCost + 2000, etd: etdReg }]
                    }
                ]
            },
            {
                code: 'indah',
                name: 'Indah Cargo',
                costs: [
                    {
                        service: 'REG',
                        description: 'Layanan Reguler',
                        cost: [{ value: regularCost - 500, etd: etdReg }]
                    }
                ]
            }
        ];
    }
}

export default new BinderByteService();
